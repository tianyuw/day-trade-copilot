"use client"

import Link from "next/link"
import { useParams, useSearchParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import { CandleCard } from "../../../components/CandleCard"
import { AICopilot, type ChatMessage } from "../../../components/AICopilot"
import { cn } from "../../../components/cn"

type StreamInit = {
  type: "init"
  mode: "realtime" | "playback"
  symbol: string
  bars: any[]
  cursor?: number
}
type StreamBar = { type: "bar"; mode: "realtime" | "playback"; symbol: string; bar: any; i?: number }
type StreamAnalysis = { type: "analysis"; mode: "realtime" | "playback"; symbol: string; result: any }
type StreamDone = { type: "done"; mode: "realtime" | "playback"; cursor?: number }
type StreamError = { type: "error"; message: string }
type StreamMessage = StreamInit | StreamBar | StreamAnalysis | StreamDone | StreamError

type AnalysisResult = {
  analysis_id: string
  timestamp: string
  symbol: string
  action: "buy_long" | "buy_short" | "ignore" | "follow_up" | "check_when_condition_meet"
  confidence: number
  reasoning: string
  pattern_name?: string | null
  breakout_price?: number | null
  watch_condition?: any
}

type MarketStatus = {
  server_time: string
  session: "pre_market" | "regular" | "after_hours" | "closed"
  is_open: boolean
  next_open: string
  next_close: string
}

type DailyBar = { t: string; o: number; h: number; l: number; c: number; v?: number }

function formatCountdown(ms: number): string {
  const clamped = Math.max(0, ms)
  const totalSeconds = Math.floor(clamped / 1000)
  const h = Math.floor(totalSeconds / 3600)
  const m = Math.floor((totalSeconds % 3600) / 60)
  const s = totalSeconds % 60
  const pad2 = (n: number) => String(n).padStart(2, "0")
  return `${pad2(h)}:${pad2(m)}:${pad2(s)}`
}

function marketLabel(session: MarketStatus["session"]): string {
  if (session === "regular") return "Regular"
  if (session === "pre_market") return "Pre-Market"
  if (session === "after_hours") return "After-Hours"
  return "Closed"
}

function marketPillClass(session: MarketStatus["session"]): string {
  if (session === "regular") return "bg-emerald-500/10 text-emerald-300 ring-emerald-500/20"
  if (session === "pre_market") return "bg-cyan-500/10 text-cyan-200 ring-cyan-500/20"
  if (session === "after_hours") return "bg-violet-500/10 text-violet-200 ring-violet-500/20"
  return "bg-white/5 text-white/50 ring-white/10"
}

function formatPSTFromRFC3339(rfc3339: string): string {
  if (!rfc3339) return ""
  const utcSeconds = Math.floor(new Date(rfc3339).getTime() / 1000)
  const pstMs = utcSeconds * 1000 - 8 * 60 * 60 * 1000
  const d = new Date(pstMs)
  const pad2 = (n: number) => String(n).padStart(2, "0")
  return `${pad2(d.getUTCHours())}:${pad2(d.getUTCMinutes())}`
}

function loadAnalysis(analysisId: string): AnalysisResult | null {
  try {
    const raw = localStorage.getItem(`analysis:${analysisId}`)
    if (!raw) return null
    return JSON.parse(raw) as AnalysisResult
  } catch {
    return null
  }
}

export default function TrackingDetailPage() {
  const params = useParams<{ symbol: string }>()
  const search = useSearchParams()
  const symbol = useMemo(() => String(params.symbol || "").toUpperCase(), [params.symbol])
  const analysisId = search.get("analysis_id")

  const [bars, setBars] = useState<any[]>([])
  const [prevClose, setPrevClose] = useState<number | null>(null)
  const [market, setMarket] = useState<MarketStatus | null>(null)
  const [lastDaily, setLastDaily] = useState<DailyBar | null>(null)
  const [wsStatus, setWsStatus] = useState<"connecting" | "open" | "closed" | "error">("closed")
  const [aiMessages, setAiMessages] = useState<ChatMessage[]>([])

  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)

  const baseHttp = useMemo(() => {
    if (typeof window === "undefined") return ""
    return process.env.NEXT_PUBLIC_BACKEND_API ?? `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
  }, [])

  const baseWs = useMemo(() => {
    if (typeof window === "undefined") return ""
    return process.env.NEXT_PUBLIC_BACKEND_WS ?? `ws://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_WS_PORT ?? "8000"}`
  }, [])

  const countdown = useMemo(() => {
    if (!market) return null
    const now = Date.now()
    const target = market.session === "regular" ? Date.parse(market.next_close) : Date.parse(market.next_open)
    if (!Number.isFinite(target)) return null
    return { label: market.session === "regular" ? "Until Close" : "Until Open", ms: target - now }
  }, [market])

  const lastPrice = useMemo(() => {
    const last = bars.length ? bars[bars.length - 1] : null
    const v = typeof last?.c === "number" ? last.c : null
    if (typeof v === "number") return v
    if (typeof lastDaily?.c === "number") return lastDaily.c
    if (typeof prevClose === "number") return prevClose
    return null
  }, [bars, lastDaily, prevClose])

  const headerChangePct = useMemo(() => {
    if (typeof lastPrice !== "number" || typeof prevClose !== "number" || prevClose === 0) return null
    return ((lastPrice - prevClose) / prevClose) * 100
  }, [lastPrice, prevClose])

  const extTag = useMemo(() => {
    if (!market) return null
    if (market.session === "pre_market") return "PRE"
    if (market.session === "after_hours") return "POST"
    return null
  }, [market])

  const closedSummary = useMemo(() => {
    if (!lastDaily) return null
    const range = Number(lastDaily.h) - Number(lastDaily.l)
    const dayPct = lastDaily.o ? ((Number(lastDaily.c) - Number(lastDaily.o)) / Number(lastDaily.o)) * 100 : null
    const gapPct =
      typeof prevClose === "number" && prevClose !== 0 ? ((Number(lastDaily.o) - prevClose) / prevClose) * 100 : null
    return { range, dayPct, gapPct }
  }, [lastDaily, prevClose])

  useEffect(() => {
    setAiMessages([
      {
        role: "system",
        content: `AI Copilot initialized for ${symbol}. Monitoring price action...`,
        time: formatPSTFromRFC3339(new Date().toISOString()),
      },
    ])
  }, [symbol])

  useEffect(() => {
    async function hydrateFromId(id: string) {
      const local = loadAnalysis(id)
      if (local) {
        setAiMessages((prev) => [
          ...prev,
          { role: "ai", content: local, time: formatPSTFromRFC3339(local.timestamp), type: "analysis" },
        ])
        return
      }

      try {
        const res = await fetch(`${baseHttp}/api/analysis/${encodeURIComponent(id)}`)
        if (!res.ok) return
        const data = (await res.json()) as AnalysisResult
        setAiMessages((prev) => [
          ...prev,
          { role: "ai", content: data, time: formatPSTFromRFC3339(data.timestamp), type: "analysis" },
        ])
      } catch (e) {}
    }
    if (analysisId) hydrateFromId(analysisId)
  }, [analysisId, baseHttp])

  useEffect(() => {
    async function fetchMarket() {
      try {
        const res = await fetch(`${baseHttp}/api/market/status`)
        if (!res.ok) throw new Error("market status failed")
        const data = (await res.json()) as MarketStatus
        setMarket(data)
      } catch {
        setMarket(null)
      }
    }
    if (!symbol) return
    fetchMarket()
    const t = window.setInterval(fetchMarket, 30_000)
    return () => window.clearInterval(t)
  }, [symbol, baseHttp])

  useEffect(() => {
    async function fetchPrevClose() {
      try {
        const asof = new Date().toISOString()
        const res = await fetch(`${baseHttp}/api/stocks/prev_close?symbols=${encodeURIComponent(symbol)}&asof=${encodeURIComponent(asof)}`)
        if (!res.ok) throw new Error("prev_close failed")
        const data = await res.json()
        setPrevClose(data.prev_close?.[symbol] ?? null)
      } catch {
        setPrevClose(null)
      }
    }
    if (symbol) fetchPrevClose()
  }, [symbol, baseHttp])

  useEffect(() => {
    const session = market?.session
    if (!symbol || !session) return

    async function fetchClosedSnapshot() {
      try {
        const res1 = await fetch(`${baseHttp}/api/stocks/bars?symbols=${encodeURIComponent(symbol)}&timeframe=1Min&limit=400`)
        if (res1.ok) {
          const data = await res1.json()
          const nextBars = (data?.bars?.[symbol] ?? []) as any[]
          if (Array.isArray(nextBars)) setBars(nextBars)
        }
      } catch (e) {}

      try {
        const res2 = await fetch(`${baseHttp}/api/stocks/bars?symbols=${encodeURIComponent(symbol)}&timeframe=1Day&limit=10`)
        if (res2.ok) {
          const data = await res2.json()
          const daily = (data?.bars?.[symbol] ?? []) as DailyBar[]
          const last = Array.isArray(daily) && daily.length ? daily[daily.length - 1] : null
          setLastDaily(last ?? null)
        }
      } catch {
        setLastDaily(null)
      }
    }

    if (session === "closed") fetchClosedSnapshot()
  }, [symbol, market?.session, baseHttp])

  useEffect(() => {
    intentionalCloseRef.current = true
    wsRef.current?.close()
    wsRef.current = null

    if (!symbol) return
    if (!market) return
    if (market?.session === "closed") {
      setWsStatus("closed")
      setAiMessages((prev) => {
        const last = prev[prev.length - 1]
        if (last && last.role === "system" && typeof last.content === "string" && last.content.includes("Market is closed")) return prev
        return [
          ...prev,
          {
            role: "system",
            content: "Market is closed. Detail page is in read-only mode (chart and AI are not updating).",
            time: formatPSTFromRFC3339(new Date().toISOString()),
          },
        ]
      })
      return
    }

    intentionalCloseRef.current = false
    setWsStatus("connecting")

    const url = `${baseWs}/ws/realtime?symbols=${encodeURIComponent(symbol)}&analyze=true`

    const ws = new WebSocket(url)
    wsRef.current = ws
    ws.onopen = () => setWsStatus("open")
    ws.onerror = () => setWsStatus("error")
    ws.onclose = () => {
      if (!intentionalCloseRef.current) setWsStatus("closed")
    }

    ws.onmessage = (ev) => {
      let msg: StreamMessage
      try {
        msg = JSON.parse(ev.data)
      } catch {
        return
      }

      if (msg.type === "error") {
        setWsStatus("error")
        setAiMessages((prev) => [
          ...prev,
          { role: "system", content: `Stream Error: ${msg.message}`, time: formatPSTFromRFC3339(new Date().toISOString()) },
        ])
        return
      }

      if (msg.type === "init") {
        if (msg.symbol === symbol) setBars(msg.bars || [])
      } else if (msg.type === "bar") {
        if (msg.symbol === symbol) setBars((prev) => [...prev, msg.bar].slice(-1000))
      } else if (msg.type === "analysis") {
        if (msg.symbol === symbol) {
          const res = msg.result as AnalysisResult
          setAiMessages((prev) => [
            ...prev,
            { role: "ai", content: res, time: formatPSTFromRFC3339(res?.timestamp ?? new Date().toISOString()), type: "analysis" },
          ])
        }
      }
    }

    return () => {
      intentionalCloseRef.current = true
      ws.close()
    }
  }, [symbol, market?.session, baseWs])

  useEffect(() => {
    if (!market) return
    if (market.session !== "pre_market" && market.session !== "after_hours") return
    setAiMessages((prev) => {
      const marker = market.session === "pre_market" ? "Pre-Market" : "After-Hours"
      const exists = prev.some((m) => m.role === "system" && typeof m.content === "string" && m.content.includes("Extended hours"))
      if (exists) return prev
      return [
        ...prev,
        {
          role: "system",
          content: `Extended hours mode (${marker}). Liquidity may be thinner and slippage risk is higher.`,
          time: formatPSTFromRFC3339(new Date().toISOString()),
        },
      ]
    })
  }, [market?.session])

  return (
    <main className="flex h-screen flex-col bg-neon-radial text-white font-sans overflow-hidden">
      <div className="flex-none border-b border-white/10 bg-black/20 backdrop-blur-xl px-6 py-4">
        <div className="mx-auto flex max-w-[1600px] flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tracking" className="rounded-xl bg-white/5 px-4 py-2 text-sm font-bold text-white/70 ring-1 ring-white/10 hover:bg-white/10 hover:text-white">
              ← Back
            </Link>
            <div className="flex items-baseline gap-3 min-w-0">
              <div className="text-2xl font-black tracking-tight">{symbol}</div>
              {typeof lastPrice === "number" && <div className="text-sm font-mono text-white/80">{lastPrice.toFixed(2)}</div>}
              {typeof headerChangePct === "number" && (
                <div className={cn("text-xs font-bold", headerChangePct >= 0 ? "text-emerald-400" : "text-red-400")}>
                  {headerChangePct >= 0 ? "+" : ""}
                  {headerChangePct.toFixed(2)}%
                </div>
              )}
            </div>

            {market && (
              <div className={cn("flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold ring-1", marketPillClass(market.session))}>
                <span className={cn("h-2 w-2 rounded-full", market.session === "regular" ? "bg-emerald-400" : market.session === "closed" ? "bg-white/30" : "bg-cyan-400")} />
                {marketLabel(market.session)}
              </div>
            )}

            {extTag && (
              <div className="rounded-full bg-white/5 px-3 py-1 text-xs font-black text-white/60 ring-1 ring-white/10">{extTag}</div>
            )}

            {countdown && (
              <div className="hidden sm:flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-xs font-mono text-white/60 ring-1 ring-white/10">
                <span className="text-white/40">{countdown.label}</span>
                <span>{formatCountdown(countdown.ms)}</span>
              </div>
            )}
            <div
              className={cn(
                "flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold ring-1",
                wsStatus === "open"
                  ? "bg-emerald-500/10 text-emerald-300 ring-emerald-500/20"
                  : wsStatus === "connecting"
                    ? "bg-cyan-500/10 text-cyan-200 ring-cyan-500/20"
                    : wsStatus === "error"
                      ? "bg-red-500/10 text-red-200 ring-red-500/20"
                      : "bg-white/5 text-white/50 ring-white/10",
              )}
            >
              <span
                className={cn(
                  "h-2 w-2 rounded-full",
                  wsStatus === "open" ? "bg-emerald-400" : wsStatus === "connecting" ? "bg-cyan-400" : wsStatus === "error" ? "bg-red-400" : "bg-white/30",
                )}
              />
              {wsStatus === "open" ? "Realtime" : wsStatus === "connecting" ? "Connecting" : wsStatus === "error" ? "Error" : "Disconnected"}
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-hidden p-6">
        <div className="mx-auto flex h-full max-w-[1600px] gap-6">
          <div className="flex-[2] min-w-0 flex flex-col gap-4">
            {market?.session === "pre_market" || market?.session === "after_hours" ? (
              <div className="rounded-2xl bg-white/5 px-4 py-3 text-xs text-white/70 ring-1 ring-white/10">
                延长交易时段：流动性更薄，滑点风险更高
              </div>
            ) : null}

            {market?.session === "closed" ? (
              <div className="rounded-2xl bg-white/5 px-4 py-3 text-sm text-white/70 ring-1 ring-white/10">
                <div className="font-bold text-white/80">Market Closed</div>
                {countdown && <div className="mt-1 text-xs font-mono text-white/60">{countdown.label}: {formatCountdown(countdown.ms)}</div>}
                <div className="mt-2 text-xs text-white/50">休市：图表已冻结在最后交易时段，AI 不进行实时更新</div>
                {lastDaily && (
                  <div className="mt-3 grid grid-cols-2 gap-2 text-xs font-mono text-white/70">
                    <div>O {Number(lastDaily.o).toFixed(2)}</div>
                    <div>H {Number(lastDaily.h).toFixed(2)}</div>
                    <div>L {Number(lastDaily.l).toFixed(2)}</div>
                    <div>C {Number(lastDaily.c).toFixed(2)}</div>
                  </div>
                )}
                {closedSummary && (
                  <div className="mt-3 grid grid-cols-3 gap-2 text-[11px] font-mono text-white/55">
                    <div>
                      Gap {typeof closedSummary.gapPct === "number" ? `${closedSummary.gapPct >= 0 ? "+" : ""}${closedSummary.gapPct.toFixed(2)}%` : "—"}
                    </div>
                    <div>
                      Day {typeof closedSummary.dayPct === "number" ? `${closedSummary.dayPct >= 0 ? "+" : ""}${closedSummary.dayPct.toFixed(2)}%` : "—"}
                    </div>
                    <div>Range {Number.isFinite(closedSummary.range) ? closedSummary.range.toFixed(2) : "—"}</div>
                  </div>
                )}
                <div className="mt-3">
                  <Link
                    href={`/dashboard?symbol=${encodeURIComponent(symbol)}`}
                    className="inline-flex items-center justify-center rounded-xl bg-white px-4 py-2 text-xs font-bold text-black hover:bg-cyan-50"
                  >
                    Open Replay Console
                  </Link>
                </div>
              </div>
            ) : null}

            <div className="relative flex-1 rounded-3xl bg-black/40 shadow-neo ring-1 ring-white/10 backdrop-blur-md overflow-hidden p-1">
              {market?.session === "regular" && (
                <div className="absolute left-4 top-4 z-20 rounded-md bg-emerald-500/15 px-2 py-1 text-[10px] font-black uppercase tracking-wider text-emerald-200 ring-1 ring-emerald-500/40">
                  LIVE
                </div>
              )}
              <CandleCard
                symbol={symbol}
                bars={bars}
                prevClose={prevClose}
                className="h-full w-full !bg-transparent !shadow-none !ring-0 !backdrop-blur-none"
                status={wsStatus === "open" ? "hot" : "normal"}
              />
            </div>
          </div>

          <div className="flex-1 min-w-[320px] hidden lg:block">
            <AICopilot symbol={symbol} messages={aiMessages} />
          </div>
        </div>
      </div>
    </main>
  )
}
