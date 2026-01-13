"use client"

import { useEffect, useMemo, useRef } from "react"
import {
  type IChartApi,
  type CandlestickData,
  type HistogramData,
  type LineData,
  type Time,
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

function barsToCandles(bars: Bar[]): CandlestickData<Time>[] {
  return bars
    .map((b) => ({
      time: toEpochSeconds(b.t) as Time,
      open: b.o,
      high: b.h,
      low: b.l,
      close: b.c,
    }))
    .sort((a, b) => Number(a.time) - Number(b.time))
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
  percentChange,
  status,
  className,
}: {
  symbol: string
  bars: Bar[]
  percentChange?: number | null
  status?: "hot" | "watch" | "normal"
  className?: string
}) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const seriesRef = useRef<ReturnType<IChartApi["addCandlestickSeries"]> | null>(null)
  const volumeSeriesRef = useRef<ReturnType<IChartApi["addHistogramSeries"]> | null>(null)

  const ema9SeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const ema21SeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const vwapSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const bbUpperSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const bbMiddleSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)
  const bbLowerSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)

  const candles = useMemo(() => barsToCandles(bars), [bars])
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
        mode: CrosshairMode.Magnet,
        vertLine: { color: "rgba(34,211,238,.35)" },
        horzLine: { color: "rgba(124,58,237,.25)" },
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
      },
      handleScroll: { mouseWheel: true, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: true },
      handleScale: { mouseWheel: true, pinch: true, axisPressedMouseMove: true },
    })
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
    if (!candles.length) return
    seriesRef.current.setData(candles)
  }, [candles])

  useEffect(() => {
    if (!volumeSeriesRef.current) return
    if (!volumes.length) return
    volumeSeriesRef.current.setData(volumes)
  }, [volumes])

  useEffect(() => {
    if (ema9SeriesRef.current && ema9.length) ema9SeriesRef.current.setData(ema9)
    if (ema21SeriesRef.current && ema21.length) ema21SeriesRef.current.setData(ema21)
    if (vwapSeriesRef.current && vwap.length) vwapSeriesRef.current.setData(vwap)
    if (bbUpperSeriesRef.current && bbUpper.length) bbUpperSeriesRef.current.setData(bbUpper)
    if (bbMiddleSeriesRef.current && bbMiddle.length) bbMiddleSeriesRef.current.setData(bbMiddle)
    if (bbLowerSeriesRef.current && bbLower.length) bbLowerSeriesRef.current.setData(bbLower)
  }, [ema9, ema21, vwap, bbUpper, bbMiddle, bbLower])

  const badge = status === "hot" ? "🔥 AI" : status === "watch" ? "⚡ Quant" : ""

  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-3xl bg-white/6 p-4 shadow-neo ring-1 ring-white/10 backdrop-blur-md",
        "transition hover:shadow-neoHover hover:drop-shadow-[0_0_18px_rgba(124,58,237,.45)]",
        className,
      )}
    >
      <div className="absolute inset-0 bg-neon-radial opacity-70" />
      <div className="relative flex items-center justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <div className="text-sm font-extrabold tracking-tight">{symbol}</div>
            {typeof percentChange === "number" && Number.isFinite(percentChange) ? (
              <div
                className={cn(
                  "rounded-full bg-black/30 px-2 py-0.5 text-[10px] font-bold ring-1 ring-white/10",
                  percentChange >= 0 ? "text-emerald-200" : "text-red-200",
                )}
              >
                {percentChange >= 0 ? "+" : ""}
                {percentChange.toFixed(2)}%
              </div>
            ) : null}
            {badge ? (
              <div className="rounded-full bg-black/30 px-2 py-0.5 text-[10px] font-bold ring-1 ring-white/10">
                {badge}
              </div>
            ) : null}
          </div>
        </div>

      </div>

      <div className="relative mt-3 h-[240px] w-full">
        <div ref={containerRef} className="h-full w-full" />
      </div>
    </div>
  )
}
