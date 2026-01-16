"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import {
  type IChartApi,
  type CandlestickData,
  type HistogramData,
  type LineData,
  type Time,
  type SeriesMarker,
  createChart,
  ColorType,
  CrosshairMode,
} from "lightweight-charts"

import { cn } from "./cn"

type Bar = {
  t: string
  o: number
  h: number
  l: number
  c: number
  v?: number
  indicators?: {
    z_score_diff?: number
    signal?: "long" | "short"
  }
}

function toEpochSeconds(rfc3339: string): number {
  return Math.floor(new Date(rfc3339).getTime() / 1000)
}

function pad2(n: number): string {
  return String(n).padStart(2, "0")
}

function formatPSTFromUtcSeconds(utcSeconds: number): string {
  const pstMs = utcSeconds * 1000 - 8 * 60 * 60 * 1000
  const d = new Date(pstMs)
  return `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`
}

function barsToCandles(
  bars: Bar[],
): CandlestickData<Time>[] {
  return bars
    .map((b) => {
      const time = toEpochSeconds(b.t) as Time
      
      return {
        time,
        open: b.o,
        high: b.h,
        low: b.l,
        close: b.c,
      }
    })
    .sort((a, b) => Number(a.time) - Number(b.time))
}

function barsToMarkers(bars: Bar[]): SeriesMarker<Time>[] {
    const markers: SeriesMarker<Time>[] = []
    
    bars.forEach((b) => {
        if (!b.indicators?.signal) return
        
        const time = toEpochSeconds(b.t) as Time
        const isLong = b.indicators.signal === "long"
        
        markers.push({
            time,
            position: 'aboveBar',
            color: isLong ? '#22c55e' : '#ef4444', // Green-500 : Red-500
            shape: 'circle',
            size: 1, // default is 1, can be adjusted
        })
    })
    
    return markers.sort((a, b) => Number(a.time) - Number(b.time))
}

function barsToVolumes(bars: Bar[]): HistogramData<Time>[] {
  return bars
    .map((b) => {
      const up = b.c >= b.o
      return {
        time: toEpochSeconds(b.t) as Time,
        value: Number(b.v ?? 0),
        color: up ? "rgba(34,211,238,.55)" : "rgba(248,113,113,.55)",
      }
    })
    .sort((a, b) => Number(a.time) - Number(b.time))
}

function barsToZScoreDiff(bars: Bar[]): LineData<Time>[] {
  return bars
    .map((b) => ({
      time: toEpochSeconds(b.t) as Time,
      value: b.indicators?.z_score_diff ?? 0,
    }))
    .sort((a, b) => Number(a.time) - Number(b.time))
}

function computeEMA(bars: Bar[], period: number): LineData<Time>[] {
  const result: LineData<Time>[] = []
  if (bars.length < period) return result

  let sum = 0
  for (let i = 0; i < period; i++) {
    sum += bars[i].c
  }
  let ema = sum / period
  result.push({ time: toEpochSeconds(bars[period - 1].t) as Time, value: ema })

  const alpha = 2 / (period + 1)
  for (let i = period; i < bars.length; i++) {
    const price = bars[i].c
    ema = price * alpha + ema * (1 - alpha)
    result.push({ time: toEpochSeconds(bars[i].t) as Time, value: ema })
  }
  return result
}

function computeBollinger(
  bars: Bar[],
  period: number,
  k: number,
): { upper: LineData<Time>[]; middle: LineData<Time>[]; lower: LineData<Time>[] } {
  const upper: LineData<Time>[] = []
  const middle: LineData<Time>[] = []
  const lower: LineData<Time>[] = []

  if (bars.length < period) return { upper, middle, lower }

  for (let i = period - 1; i < bars.length; i++) {
    let sum = 0
    for (let j = 0; j < period; j++) {
      sum += bars[i - j].c
    }
    const sma = sum / period
    let sumSq = 0
    for (let j = 0; j < period; j++) {
      sumSq += Math.pow(bars[i - j].c - sma, 2)
    }
    const stdDev = Math.sqrt(sumSq / period)

    const time = toEpochSeconds(bars[i].t) as Time
    middle.push({ time, value: sma })
    upper.push({ time, value: sma + k * stdDev })
    lower.push({ time, value: sma - k * stdDev })
  }
  return { upper, middle, lower }
}

function computeVWAP(bars: Bar[]): LineData<Time>[] {
  const result: LineData<Time>[] = []
  if (!bars.length) return result

  let cumTPV = 0
  let cumVol = 0

  for (let i = 0; i < bars.length; i++) {
    const b = bars[i]
    const tp = (b.h + b.l + b.c) / 3
    const vol = b.v ?? 0
    cumTPV += tp * vol
    cumVol += vol
    if (cumVol > 0) {
      result.push({ time: toEpochSeconds(b.t) as Time, value: cumTPV / cumVol })
    }
  }
  return result
}

export function CandleCard({
  symbol,
  bars,
  prevClose,
  percentChange,
  status,
  className,
  isAnalyzing,
  onPause,
  onResume,
  onAnalyze,
}: {
  symbol: string
  bars: Bar[]
  prevClose?: number | null
  percentChange?: number | null
  status?: "hot" | "watch" | "normal"
  className?: string
  isAnalyzing?: boolean
  onPause?: () => void
  onResume?: () => void
  onAnalyze?: (time: string) => Promise<void>
}) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const seriesRef = useRef<ReturnType<IChartApi["addCandlestickSeries"]> | null>(null)
  const volumeSeriesRef = useRef<ReturnType<IChartApi["addHistogramSeries"]> | null>(null)
  const zScoreSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const ema9SeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const ema21SeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const vwapSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const bbUpperSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const bbMiddleSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const bbLowerSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  
  const [lastAnalyzedTime, setLastAnalyzedTime] = useState<number | null>(null)

  // Monitor for signals and trigger analysis
  useEffect(() => {
    if (bars.length === 0) return
    const lastBar = bars[bars.length - 1]
    
    // Check if we have a signal on the latest bar
    if (lastBar.indicators?.signal && onPause && onAnalyze && onResume) {
        const time = toEpochSeconds(lastBar.t)
        
        // Only analyze if we haven't analyzed this bar yet
        if (lastAnalyzedTime !== time) {
            setLastAnalyzedTime(time)
            
            // Execute Sequential Logic: Pause -> Analyze -> Resume
            const runAnalysis = async () => {
                onPause()
                try {
                    await onAnalyze(lastBar.t)
                } finally {
                    // Auto-resume after analysis is done (or failed)
                    onResume()
                }
            }
            
            runAnalysis()
        }
    }
  }, [bars, onPause, onAnalyze, onResume, lastAnalyzedTime])

  const candles = useMemo(() => barsToCandles(bars), [bars])
  const markers = useMemo(() => barsToMarkers(bars), [bars])
  const volumes = useMemo(() => barsToVolumes(bars), [bars])

  const ema9 = useMemo(() => computeEMA(bars, 9), [bars])
  const ema21 = useMemo(() => computeEMA(bars, 21), [bars])
  const vwap = useMemo(() => computeVWAP(bars), [bars])
  const { upper: bbUpper, middle: bbMiddle, lower: bbLower } = useMemo(
    () => computeBollinger(bars, 20, 2),
    [bars],
  )

  useEffect(() => {
    if (!containerRef.current) return
    if (chartRef.current) return

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: "rgba(0,0,0,0)" },
        textColor: "rgba(255,255,255,.8)",
        fontFamily: "ui-sans-serif, system-ui, -apple-system",
        attributionLogo: false,
      },
      grid: {
        vertLines: { color: "rgba(255,255,255,.06)" },
        horzLines: { color: "rgba(255,255,255,.06)" },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: {
          color: "rgba(34,211,238,0.5)",
          width: 1,
          style: 1, // LineStyle.Dotted
          labelBackgroundColor: "#22d3ee",
        },
        horzLine: {
          color: "rgba(34,211,238,0.5)",
          width: 1,
          style: 1, // LineStyle.Dotted
          labelBackgroundColor: "#22d3ee",
        },
      },
      timeScale: {
        borderColor: "rgba(255,255,255,.08)",
        timeVisible: true,
        secondsVisible: false,
        tickMarkFormatter: (time: Time) => {
          const utcSeconds = typeof time === "number" ? time : Number.NaN
          if (!Number.isFinite(utcSeconds)) return null
          return formatPSTFromUtcSeconds(utcSeconds)
        },
      },
      localization: {
        dateFormat: "yyyy-MM-dd",
        timeFormatter: (time: Time) => {
          const utcSeconds = typeof time === "number" ? time : Number.NaN
          if (!Number.isFinite(utcSeconds)) return ""
          return formatPSTFromUtcSeconds(utcSeconds)
        },
      },
      rightPriceScale: {
        borderColor: "rgba(255,255,255,.08)",
        scaleMargins: { top: 0.08, bottom: 0.28 },
        visible: true, // Main chart scale
      },
      handleScroll: { mouseWheel: true, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: true },
      handleScale: { mouseWheel: true, pinch: true, axisPressedMouseMove: true },
    })
    
    // Create Price Scale for Indicator (bottom pane)
    // We want main chart to take top 65% and indicator take bottom 30%
    // Main chart margins: top: 0.05, bottom: 0.35
    // Indicator chart margins: top: 0.70, bottom: 0
    
    // Configure Main Price Scale
    chart.priceScale("right").applyOptions({
        scaleMargins: { top: 0.08, bottom: 0.28 },
    })
    
    // We don't need 'left' scale anymore
    chart.priceScale("left").applyOptions({ visible: false })

    const series = chart.addCandlestickSeries({
      upColor: "rgba(34,211,238,1)",
      downColor: "rgba(248,113,113,1)",
      borderUpColor: "rgba(34,211,238,1)",
      borderDownColor: "rgba(248,113,113,1)",
      wickUpColor: "rgba(34,211,238,.9)",
      wickDownColor: "rgba(248,113,113,.9)",
    })

    const ema9Series = chart.addLineSeries({
      color: "rgba(34,197,94,0.9)", // Green
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    })

    const ema21Series = chart.addLineSeries({
      color: "rgba(248,113,113,0.9)", // Red
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    })

    const vwapSeries = chart.addLineSeries({
      color: "rgba(248,250,252,0.95)", // White
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    })

    const bbUpperSeries = chart.addLineSeries({
      color: "rgba(168,85,247,0.8)", // Purple
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    })

    const bbMiddleSeries = chart.addLineSeries({
      color: "rgba(59,130,246,0.8)", // Blue
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    })

    const bbLowerSeries = chart.addLineSeries({
      color: "rgba(250,204,21,0.8)", // Yellow
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
    })

    const volumeSeries = chart.addHistogramSeries({
      priceScaleId: "",
      priceFormat: { type: "volume" },
      lastValueVisible: false,
      priceLineVisible: false,
    })
    chart.priceScale("").applyOptions({
      scaleMargins: { top: 0.78, bottom: 0 },
      visible: false,
    })
    
    chartRef.current = chart
    seriesRef.current = series
    volumeSeriesRef.current = volumeSeries

    ema9SeriesRef.current = ema9Series
    ema21SeriesRef.current = ema21Series
    vwapSeriesRef.current = vwapSeries
    bbUpperSeriesRef.current = bbUpperSeries
    bbMiddleSeriesRef.current = bbMiddleSeries
    bbLowerSeriesRef.current = bbLowerSeries

    const ro = new ResizeObserver(() => {
      if (!containerRef.current || !chartRef.current) return
      chartRef.current.applyOptions({
        width: containerRef.current.clientWidth,
        height: containerRef.current.clientHeight,
      })
    })
    ro.observe(containerRef.current)

    return () => ro.disconnect()
  }, [])

  useEffect(() => {
    if (!seriesRef.current) return
    seriesRef.current.setData(candles)
    seriesRef.current.setMarkers(markers)
  }, [candles, markers])

  useEffect(() => {
    if (!volumeSeriesRef.current) return
    volumeSeriesRef.current.setData(volumes)
  }, [volumes])

  useEffect(() => {
    // Helper to safely set data or clear series
    const updateSeries = (seriesRef: any, data: any[]) => {
      if (!seriesRef.current) return
      seriesRef.current.setData(data)
    }

    updateSeries(ema9SeriesRef, ema9)
    updateSeries(ema21SeriesRef, ema21)
    updateSeries(vwapSeriesRef, vwap)
    updateSeries(bbUpperSeriesRef, bbUpper)
    updateSeries(bbMiddleSeriesRef, bbMiddle)
    updateSeries(bbLowerSeriesRef, bbLower)
  }, [ema9, ema21, vwap, bbUpper, bbMiddle, bbLower])

  const [overlayData, setOverlayData] = useState<{
    ema9?: number
    ema21?: number
    vwap?: number
    bbUpper?: number
    bbMiddle?: number
    bbLower?: number
    volume?: number
    price?: number
    time?: number
  } | null>(null)

  useEffect(() => {
    if (!chartRef.current || !seriesRef.current) return

    const handleCrosshairMove = (param: any) => {
      if (
        param.point === undefined ||
        !param.time ||
        param.point.x < 0 ||
        param.point.x > containerRef.current!.clientWidth ||
        param.point.y < 0 ||
        param.point.y > containerRef.current!.clientHeight
      ) {
        // Crosshair is out of chart, use latest bar data
        if (candles.length > 0) {
          const lastIdx = candles.length - 1
          const time = Number(candles[lastIdx].time)
          
          // Find indicator values for this time
          const findVal = (data: LineData<Time>[]) => data.find((d) => Number(d.time) === time)?.value
          const findVol = (data: HistogramData<Time>[]) => data.find((d) => Number(d.time) === time)?.value
          const findPrice = (data: CandlestickData<Time>[]) => data.find((d) => Number(d.time) === time)?.close

          setOverlayData({
            ema9: findVal(ema9),
            ema21: findVal(ema21),
            vwap: findVal(vwap),
            bbUpper: findVal(bbUpper),
            bbMiddle: findVal(bbMiddle),
            bbLower: findVal(bbLower),
            volume: findVol(volumes),
            price: findPrice(candles),
            time: time,
          })
        } else {
            setOverlayData(null)
        }
        return
      }

      // User hovering
      const time = param.time as number
      const seriesData = param.seriesData
      const price = seriesData.get(seriesRef.current!)?.close || seriesData.get(seriesRef.current!)?.value

      // Find indicator values for this time
      const findVal = (data: LineData<Time>[]) => data.find((d) => Number(d.time) === time)?.value
      const findVol = (data: HistogramData<Time>[]) => data.find((d) => Number(d.time) === time)?.value

      setOverlayData({
        ema9: findVal(ema9),
        ema21: findVal(ema21),
        vwap: findVal(vwap),
        bbUpper: findVal(bbUpper),
        bbMiddle: findVal(bbMiddle),
        bbLower: findVal(bbLower),
        volume: findVol(volumes),
        price: typeof price === 'number' ? price : undefined,
        time: time,
      })
    }

    chartRef.current.subscribeCrosshairMove(handleCrosshairMove)
    
    // Initial data set
    if (candles.length > 0) {
         const lastIdx = candles.length - 1
          const time = Number(candles[lastIdx].time)
          const findVal = (data: LineData<Time>[]) => data.find((d) => Number(d.time) === time)?.value
          const findVol = (data: HistogramData<Time>[]) => data.find((d) => Number(d.time) === time)?.value
          const findPrice = (data: CandlestickData<Time>[]) => data.find((d) => Number(d.time) === time)?.close

          setOverlayData({
            ema9: findVal(ema9),
            ema21: findVal(ema21),
            vwap: findVal(vwap),
            bbUpper: findVal(bbUpper),
            bbMiddle: findVal(bbMiddle),
            bbLower: findVal(bbLower),
            volume: findVol(volumes),
            price: findPrice(candles),
            time: time,
          })
    } else {
        setOverlayData(null)
    }

    return () => {
      chartRef.current?.unsubscribeCrosshairMove(handleCrosshairMove)
    }
  }, [candles, ema9, ema21, vwap, bbUpper, bbMiddle, bbLower, volumes])

  const currentPrice = overlayData?.price ?? (candles.length > 0 ? candles[candles.length - 1].close : null)
  const priceChange = (typeof currentPrice === 'number' && typeof prevClose === 'number') 
    ? ((currentPrice - prevClose) / prevClose * 100) 
    : null


  const badge = status === "hot" ? "🔥 AI" : status === "watch" ? "⚡ Quant" : ""

  return (
    <div
      className={cn(
        "group relative flex flex-col overflow-hidden rounded-3xl bg-white/6 p-4 shadow-neo ring-1 ring-white/10 backdrop-blur-md",
        "transition hover:shadow-neoHover hover:drop-shadow-[0_0_18px_rgba(124,58,237,.45)]",
        className,
      )}
    >
      <div className="absolute inset-0 bg-neon-radial opacity-70" />
      
      {isAnalyzing && (
        <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
            <div className="h-12 w-12 rounded-full border-4 border-white/10 border-t-cyan-400 animate-spin mb-4" />
            <div className="text-cyan-400 font-mono font-bold animate-pulse">AI Analyzing Signal...</div>
        </div>
      )}
      
      <div className="absolute top-4 left-4 z-10 pointer-events-none select-none flex flex-col gap-1">
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-white tracking-tight">{symbol}</span>
          {priceChange !== null && (
            <span
              className={cn(
                "text-lg font-medium",
                priceChange >= 0 ? "text-emerald-400" : "text-red-400"
              )}
            >
              {priceChange >= 0 ? "+" : ""}
              {priceChange.toFixed(2)}%
            </span>
          )}
        </div>
        
        {overlayData && (
          <div className="flex flex-col gap-0.5 text-xs font-mono font-medium">
            {overlayData.ema9 !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-white/40 w-8">EMA9</span>
                <span className="text-emerald-400">{overlayData.ema9.toFixed(2)}</span>
              </div>
            )}
            {overlayData.ema21 !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-white/40 w-8">EMA21</span>
                <span className="text-red-400">{overlayData.ema21.toFixed(2)}</span>
              </div>
            )}
            {overlayData.volume !== undefined && (
               <div className="flex items-center gap-2">
                 <span className="text-white/40 w-8">Vol</span>
                 <span className={cn(
                   (overlayData.price !== undefined && (candles.find(c => Number(c.time) === overlayData.time)?.open || 0) <= overlayData.price) 
                     ? "text-cyan-400" 
                     : "text-red-400"
                 )}>
                   {overlayData.volume.toLocaleString()}
                 </span>
               </div>
            )}
            {overlayData.vwap !== undefined && (
              <div className="flex items-center gap-2 mt-1">
                <span className="text-white/60">VWAP</span>
                <span className="text-white">{overlayData.vwap.toFixed(2)}</span>
              </div>
            )}
             {overlayData.bbUpper !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-white/40 w-8">BB</span>
                <span className="text-purple-400">{overlayData.bbUpper.toFixed(2)}</span>
                <span className="text-blue-400">{overlayData.bbMiddle?.toFixed(2)}</span>
                <span className="text-yellow-400">{overlayData.bbLower?.toFixed(2)}</span>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="relative flex items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            
            {/* Old header content removed/hidden */}
          </div>
        </div>

      </div>

      <div className="relative mt-3 h-full w-full flex-1 min-h-[400px]">
        <div ref={containerRef} className="h-full w-full" />
      </div>
    </div>
  )
}
