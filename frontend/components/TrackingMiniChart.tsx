"use client"

import { useEffect, useMemo, useRef } from "react"
import {
  type CandlestickData,
  ColorType,
  CrosshairMode,
  createChart,
  type IChartApi,
  type LineData,
  type Time,
} from "lightweight-charts"

import { cn } from "./cn"

type Bar = { t: string; o: number; h: number; l: number; c: number }

const ptTimeFormatter = new Intl.DateTimeFormat("en-US", {
  timeZone: "America/Los_Angeles",
  hour: "2-digit",
  minute: "2-digit",
  hour12: false,
})

function toEpochSeconds(rfc3339: string): number | null {
  const ms = new Date(rfc3339).getTime()
  if (!Number.isFinite(ms)) return null
  return Math.floor(ms / 1000)
}

function formatPTFromUtcSeconds(utcSeconds: number): string {
  try {
    return ptTimeFormatter.format(new Date(utcSeconds * 1000))
  } catch {
    const ptMs = utcSeconds * 1000 - 8 * 60 * 60 * 1000
    const d = new Date(ptMs)
    const pad2 = (n: number) => String(n).padStart(2, "0")
    return `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`
  }
}

function floorToMinute(ms: number): number {
  return Math.floor(ms / 60_000) * 60_000
}

function floorToBucket(ms: number, bucketMinutes: number): number {
  const stepMs = Math.max(1, Math.floor(bucketMinutes)) * 60_000
  return Math.floor(ms / stepMs) * stepMs
}

function windowLastMinutes(bars: Bar[], minutes: number, anchorTimeRfc3339?: string, bucketMinutes = 1): Bar[] {
  if (bars.length === 0) return []

  const nowMs = Date.now()
  const lastBarMs = new Date(bars[bars.length - 1]!.t).getTime()
  const anchorOverrideMs = anchorTimeRfc3339 ? new Date(anchorTimeRfc3339).getTime() : NaN
  const anchorMs = Number.isFinite(anchorOverrideMs) ? anchorOverrideMs : Number.isFinite(lastBarMs) ? lastBarMs : nowMs
  const stepMs = Math.max(1, Math.floor(bucketMinutes)) * 60_000
  const bucketCount = Math.max(1, Math.ceil(minutes / Math.max(1, Math.floor(bucketMinutes))))
  const endMs = floorToBucket(Number.isFinite(anchorMs) ? anchorMs : nowMs, bucketMinutes)
  const startMs = endMs - (bucketCount - 1) * stepMs

  const byBucket = new Map<number, Bar>()
  for (const b of bars) {
    const ms = floorToBucket(new Date(b.t).getTime(), bucketMinutes)
    if (!Number.isFinite(ms)) continue
    if (ms < startMs - stepMs * 2 || ms > endMs + stepMs * 2) continue
    byBucket.set(ms, b)
  }

  let seed: number | null = null
  const sortedBars = [...bars]
    .map((b) => ({ b, ms: new Date(b.t).getTime() }))
    .filter((x) => Number.isFinite(x.ms))
    .sort((a, b) => a.ms - b.ms)

  for (let i = sortedBars.length - 1; i >= 0; i--) {
    if (sortedBars[i]!.ms <= startMs) {
      seed = sortedBars[i]!.b.c
      break
    }
  }
  if (seed == null) {
    const first = sortedBars.find((x) => x.ms >= startMs && x.ms <= endMs)?.b
    if (first) seed = typeof first.o === "number" && first.o > 0 ? first.o : first.c
  }
  if (seed == null) return []

  const out: Bar[] = []
  let prevClose = seed
  for (let ms = startMs; ms <= endMs; ms += stepMs) {
    const bar = byBucket.get(ms)
    if (bar) {
      out.push(bar)
      prevClose = bar.c
      continue
    }
    out.push({
      t: new Date(ms).toISOString(),
      o: prevClose,
      h: prevClose,
      l: prevClose,
      c: prevClose,
    })
  }
  return out
}

export function TrackingMiniChart({
  bars,
  className,
  windowMinutes = 120,
  anchorTimeRfc3339,
  bucketMinutes = 1,
}: {
  bars: Bar[]
  className?: string
  windowMinutes?: number
  anchorTimeRfc3339?: string
  bucketMinutes?: number
}) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const candleSeriesRef = useRef<ReturnType<IChartApi["addCandlestickSeries"]> | null>(null)
  const pctSeriesRef = useRef<ReturnType<IChartApi["addLineSeries"]> | null>(null)

  const windowBars = useMemo(
    () => windowLastMinutes(bars, windowMinutes, anchorTimeRfc3339, bucketMinutes),
    [anchorTimeRfc3339, bars, bucketMinutes, windowMinutes],
  )

  const candles = useMemo(() => {
    const out: CandlestickData<Time>[] = []
    for (const b of windowBars) {
      const t = toEpochSeconds(b.t)
      if (t == null) continue
      out.push({ time: t as Time, open: b.o, high: b.h, low: b.l, close: b.c })
    }
    out.sort((a, b) => Number(a.time) - Number(b.time))
    return out
  }, [windowBars])

  const pctLine = useMemo(() => {
    const first = windowBars[0]
    const base = typeof first?.o === "number" && first.o > 0 ? first.o : typeof first?.c === "number" && first.c > 0 ? first.c : null
    if (!base) return [] as LineData<Time>[]

    const out: LineData<Time>[] = []
    for (const b of windowBars) {
      const t = toEpochSeconds(b.t)
      if (t == null) continue
      const pct = ((b.c - base) / base) * 100
      out.push({ time: t as Time, value: pct })
    }
    out.sort((a, b) => Number(a.time) - Number(b.time))
    return out
  }, [windowBars])

  useEffect(() => {
    if (!containerRef.current) return
    if (chartRef.current) return

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: "rgba(0,0,0,0)" },
        textColor: "rgba(255,255,255,.7)",
        fontFamily: "ui-sans-serif, system-ui, -apple-system",
        attributionLogo: false,
      },
      grid: {
        vertLines: { color: "rgba(255,255,255,.05)" },
        horzLines: { color: "rgba(255,255,255,.05)" },
      },
      crosshair: { mode: CrosshairMode.Hidden },
      timeScale: {
        visible: true,
        borderVisible: false,
        timeVisible: true,
        secondsVisible: false,
        ticksVisible: true,
        tickMarkFormatter: (time: Time) => {
          const utcSeconds = typeof time === "number" ? time : null
          if (utcSeconds == null) return ""
          return formatPTFromUtcSeconds(utcSeconds)
        },
      },
      localization: {
        timeFormatter: (time: Time) => {
          const utcSeconds = typeof time === "number" ? time : null
          if (utcSeconds == null) return ""
          return formatPTFromUtcSeconds(utcSeconds)
        },
      },
      leftPriceScale: {
        visible: true,
        borderVisible: false,
        scaleMargins: { top: 0.05, bottom: 0.05 },
      },
      rightPriceScale: {
        visible: true,
        borderVisible: false,
        scaleMargins: { top: 0.05, bottom: 0.05 },
      },
      handleScroll: false,
      handleScale: false,
    })

    const candlesSeries = chart.addCandlestickSeries({
      priceScaleId: "left",
      upColor: "rgba(34,211,238,1)",
      downColor: "rgba(248,113,113,1)",
      borderUpColor: "rgba(34,211,238,1)",
      borderDownColor: "rgba(248,113,113,1)",
      wickUpColor: "rgba(34,211,238,.9)",
      wickDownColor: "rgba(248,113,113,.9)",
      lastValueVisible: false,
      priceLineVisible: false,
      priceFormat: { type: "price", precision: 2, minMove: 0.01 },
    })

    const pctSeries = chart.addLineSeries({
      priceScaleId: "right",
      color: "rgba(255,255,255,0.16)",
      lineWidth: 1,
      crosshairMarkerVisible: false,
      lastValueVisible: false,
      priceLineVisible: false,
      priceFormat: {
        type: "custom",
        formatter: (p: number) => `${p >= 0 ? "+" : ""}${p.toFixed(2)}%`,
      },
    })

    chartRef.current = chart
    candleSeriesRef.current = candlesSeries
    pctSeriesRef.current = pctSeries

    const ro = new ResizeObserver(() => {
      if (!containerRef.current || !chartRef.current) return
      chartRef.current.applyOptions({
        width: containerRef.current.clientWidth,
        height: containerRef.current.clientHeight,
      })
      chartRef.current.timeScale().fitContent()
    })
    ro.observe(containerRef.current)

    return () => ro.disconnect()
  }, [])

  useEffect(() => {
    candleSeriesRef.current?.setData(candles)
    pctSeriesRef.current?.setData(pctLine)
    chartRef.current?.timeScale().fitContent()
  }, [candles, pctLine])

  return (
    <div className={cn("relative h-24 w-full overflow-hidden", className)}>
      <div ref={containerRef} className="absolute inset-0 h-full w-full" />
    </div>
  )
}
