"use client"

import Link from "next/link"
import { useParams, useSearchParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import { cn } from "../../../components/cn"
import { TickerConsole } from "../../../components/TickerConsole"
import type { ChatMessage } from "../../../components/AICopilot"
import { useAnalysisMarkers } from "../../../components/hooks/useAnalysisMarkers"
import { useBackendBaseUrls } from "../../../components/hooks/useBackendBaseUrls"
import { type MarketStatus, useMarketStatus } from "../../../components/hooks/useMarketStatus"
import { usePrevClose } from "../../../components/hooks/usePrevClose"

type StreamInit = { type: "init"; mode: "realtime"; symbol: string; bars: any[]; cursor?: number }
type StreamBar = { type: "bar"; mode: "realtime"; symbol: string; analysis_trigger_reason?: any; bar: any; i?: number }
type StreamAnalysis = { type: "analysis"; mode: "realtime"; symbol: string; trigger_reason?: any; result: any }
type StreamState = {
  type: "state"
  mode: "realtime"
  symbol: string
  state: string
  in_position: boolean
  contracts_total?: number | null
  contracts_remaining?: number | null
  trade_id?: string | null
  option?: { right: "call" | "put"; expiration: string; strike: number } | null
  option_symbol?: string | null
}
type StreamPosition = { type: "position"; mode: "realtime"; symbol: string; trigger_reason?: any; result: any }
type StreamDone = { type: "done"; mode: "realtime"; cursor?: number }
type StreamError = { type: "error"; message: string }
type StreamMessage = StreamInit | StreamBar | StreamAnalysis | StreamState | StreamPosition | StreamDone | StreamError

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
  const [lastDaily, setLastDaily] = useState<DailyBar | null>(null)
  const [prevSession, setPrevSession] = useState<{ open: number | null; close: number | null; openToClosePct: number | null } | null>(null)
  const [wsStatus, setWsStatus] = useState<"connecting" | "open" | "closed" | "error">("closed")
  const [aiMessages, setAiMessages] = useState<ChatMessage[]>([])

  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const barsRef = useRef<any[]>([])
  const lastStreamStateRef = useRef<{
    contracts_remaining: number | null
    option: StreamState["option"] | null
    option_symbol: string | null
  }>({ contracts_remaining: null, option: null, option_symbol: null })

  const { baseHttp, baseWs } = useBackendBaseUrls()
  const { market } = useMarketStatus(baseHttp, { enabled: !!symbol })
  const asof = useMemo(() => (symbol ? new Date().toISOString() : null), [symbol])
  const { prevClose } = usePrevClose(baseHttp, symbol, { asof, enabled: !!symbol })
  const { recordAnalysisMarker, applyMarkersToBars } = useAnalysisMarkers()

  const isOffHours = useMemo(() => !!market && market.session !== "regular", [market])
  const isOffHoursReadOnly = isOffHours

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

  const headerDisplayPrice = useMemo(() => {
    if (!isOffHoursReadOnly) return lastPrice
    if (typeof prevSession?.close === "number") return prevSession.close
    if (typeof lastDaily?.c === "number") return lastDaily.c
    return lastPrice
  }, [isOffHoursReadOnly, lastDaily?.c, lastPrice, prevSession?.close])

  const headerDisplayPct = useMemo(() => {
    if (!isOffHoursReadOnly) return headerChangePct
    if (typeof prevSession?.open === "number" && typeof prevSession?.close === "number" && prevSession.open !== 0) {
      return ((prevSession.close - prevSession.open) / prevSession.open) * 100
    }
    if (typeof lastDaily?.o === "number" && typeof lastDaily?.c === "number" && lastDaily.o !== 0) {
      return ((lastDaily.c - lastDaily.o) / lastDaily.o) * 100
    }
    return null
  }, [headerChangePct, isOffHoursReadOnly, lastDaily?.c, lastDaily?.o, prevSession?.close, prevSession?.open])

  const extTag = useMemo(() => {
    if (!market) return null
    if (market.session === "pre_market") return "PRE"
    if (market.session === "after_hours") return "POST"
    return null
  }, [market])

  useEffect(() => {
    barsRef.current = bars
  }, [bars])

  useEffect(() => {
    barsRef.current = []
    lastStreamStateRef.current = { contracts_remaining: null, option: null, option_symbol: null }
    setAiMessages([
      {
        role: "system",
        content: `AI Copilot initialized for ${symbol}. Monitoring price action...`,
        time: formatPSTFromRFC3339(new Date().toISOString()),
      },
    ])
  }, [symbol])

  useEffect(() => {
    async function hydrateHistory() {
      try {
        const res = await fetch(`${baseHttp}/api/ai/history/${encodeURIComponent(symbol)}`)
        if (!res.ok) return
        const data = await res.json()
        const analysis: any[] = Array.isArray(data?.analysis) ? data.analysis : []
        const positions: any[] = Array.isArray(data?.positions) ? data.positions : []
        const items: Array<{ ts: string; kind: "analysis" | "position"; payload: any }> = []
        for (const a of analysis) {
          if (a && typeof a === "object") {
            const ts = String(a.bar_time ?? a.timestamp ?? "")
            if (ts) recordAnalysisMarker(ts, a)
            items.push({ ts: String(a.timestamp ?? ""), kind: "analysis", payload: a })
          }
        }
        for (const p of positions) {
          if (p && typeof p === "object") items.push({ ts: String(p.timestamp ?? p.bar_time ?? ""), kind: "position", payload: p })
        }
        items.sort((x, y) => Date.parse(x.ts) - Date.parse(y.ts))

        setAiMessages((prev) => {
          const base = prev.slice(0, 1)
          const mapped = items.map((it) => {
            if (it.kind === "analysis") {
              return { role: "ai" as const, content: it.payload, time: formatPSTFromRFC3339(it.ts), type: "analysis" as const }
            }
            const d = it.payload?.decision
            const pos = it.payload?.position
            const inferredAction = d?.action ?? (pos ? "requested" : "hold")
            const summaryParts = [`POSITION_MGMT: ${inferredAction}`, String(d?.reasoning ?? "")].filter(Boolean)
            summaryParts.push(`underlying_symbol=${symbol}`)
            if (typeof pos?.contracts_remaining === "number") summaryParts.push(`contracts=${pos.contracts_remaining}`)
            if (typeof pos?.direction === "string") summaryParts.push(`direction=${pos.direction}`)
            if (pos?.option) {
              const right = String(pos.option?.right ?? "").toUpperCase()
              const exp = String(pos.option?.expiration ?? "")
              const strike = typeof pos.option?.strike === "number" ? String(pos.option.strike) : ""
              const optLine = [right, exp, strike].filter(Boolean).join(" ")
              if (optLine) summaryParts.push(`option=${optLine}`)
            }
            if (typeof it.payload?.option_symbol === "string" && it.payload.option_symbol) {
              summaryParts.push(`option_symbol=${it.payload.option_symbol}`)
            }
            const lastReqBar = Array.isArray(it.payload?.ohlcv_1m) ? it.payload.ohlcv_1m[it.payload.ohlcv_1m.length - 1] : null
            const lastPx =
              typeof lastReqBar?.c === "number"
                ? lastReqBar.c
                : typeof lastReqBar?.close === "number"
                  ? lastReqBar.close
                  : null
            if (lastPx != null) summaryParts.push(`underlying_price=${lastPx}`)
            if (pos?.risk) {
              if (pos.risk.stop_loss_premium != null) summaryParts.push(`stop_loss=${pos.risk.stop_loss_premium}`)
              if (pos.risk.take_profit_premium != null) summaryParts.push(`take_profit=${pos.risk.take_profit_premium}`)
              if (pos.risk.time_stop_minutes != null) summaryParts.push(`time_stop_minutes=${pos.risk.time_stop_minutes}`)
            }
            if (d?.exit?.contracts_to_close) summaryParts.push(`contracts=${d.exit.contracts_to_close}`)
            if (d?.adjustments?.new_stop_loss_premium != null) summaryParts.push(`stop_loss=${d.adjustments.new_stop_loss_premium}`)
            if (d?.adjustments?.new_take_profit_premium != null) summaryParts.push(`take_profit=${d.adjustments.new_take_profit_premium}`)
            if (d?.adjustments?.new_time_stop_minutes != null) summaryParts.push(`time_stop_minutes=${d.adjustments.new_time_stop_minutes}`)
            const optPx = it.payload?.position_option_quote?.asof_price
            summaryParts.push(`option_price=${optPx ?? "N/A"}`)
            return { role: "ai" as const, content: summaryParts.join("\n"), time: formatPSTFromRFC3339(it.ts) }
          })
          return [...base, ...mapped]
        })
        setBars((prev) => applyMarkersToBars(prev))
      } catch {}
    }

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
      } catch {}
    }

    if (!symbol) return
    hydrateHistory()
    if (analysisId) hydrateFromId(analysisId)
  }, [analysisId, baseHttp, symbol])

  useEffect(() => {
    const session = market?.session
    if (!symbol || !session) return

    async function fetchOffHoursSnapshot() {
      const start = market?.last_rth_open
      const end = market?.last_rth_close
      if (start && end) {
        try {
          const res1 = await fetch(
            `${baseHttp}/api/stocks/bars?symbols=${encodeURIComponent(symbol)}&timeframe=5Min&start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}&limit=10000`,
          )
          if (res1.ok) {
            const data = await res1.json()
            const nextBars = (data?.bars?.[symbol] ?? []) as any[]
            if (Array.isArray(nextBars)) {
              const withMarkers = applyMarkersToBars(nextBars)
              setBars(withMarkers)
              const sorted = [...nextBars]
                .map((b) => ({ b, ms: Date.parse(String(b?.t ?? "")) }))
                .filter((x) => Number.isFinite(x.ms))
                .sort((a, b) => a.ms - b.ms)
                .map((x) => x.b)
              const first = sorted.length ? sorted[0] : null
              const last = sorted.length ? sorted[sorted.length - 1] : null
              const o = typeof first?.o === "number" ? (first.o as number) : null
              const c = typeof last?.c === "number" ? (last.c as number) : null
              const pct = typeof o === "number" && typeof c === "number" && o !== 0 ? ((c - o) / o) * 100 : null
              setPrevSession({ open: o, close: c, openToClosePct: pct })
            }
          }
        } catch {}
      }

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

    if (isOffHoursReadOnly) fetchOffHoursSnapshot()
    else {
      setPrevSession(null)
    }
  }, [symbol, isOffHoursReadOnly, market?.last_rth_open, market?.last_rth_close, market?.session, baseHttp, applyMarkersToBars])

  useEffect(() => {
    intentionalCloseRef.current = true
    wsRef.current?.close()
    wsRef.current = null

    if (!symbol) return
    if (!market?.session) return
    if (isOffHoursReadOnly) {
      setWsStatus("closed")
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
        if (msg.symbol === symbol) setBars(applyMarkersToBars(msg.bars || []))
      } else if (msg.type === "bar") {
        if (msg.symbol === symbol) {
          const hasTrigger = Boolean((msg as any).analysis_trigger_reason)
          const o = typeof (msg as any)?.bar?.o === "number" ? (msg as any).bar.o : null
          const c = typeof (msg as any)?.bar?.c === "number" ? (msg as any).bar.c : null
          const color: "green" | "red" = typeof o === "number" && typeof c === "number" && c >= o ? "green" : "red"
          const nextBar = hasTrigger ? { ...(msg as any).bar, ui_marker: { kind: "analysis", color } } : msg.bar
          setBars((prev) => applyMarkersToBars([...prev, nextBar].slice(-1000)))
        }
      } else if (msg.type === "analysis") {
        if (msg.symbol === symbol) {
          const res = msg.result as AnalysisResult
          const ts = String((res as any)?.bar_time ?? res?.timestamp ?? "")
          if (ts) recordAnalysisMarker(ts, res)
          setBars((prev) => applyMarkersToBars(prev))
          setAiMessages((prev) => [
            ...prev,
            {
              role: "ai",
              content: res,
              time: formatPSTFromRFC3339(res?.timestamp ?? new Date().toISOString()),
              type: "analysis",
              trigger_reason: (msg as any)?.trigger_reason as any,
            },
          ])
        }
      } else if (msg.type === "state") {
        if (msg.symbol === symbol) {
          lastStreamStateRef.current = {
            contracts_remaining: typeof (msg as any).contracts_remaining === "number" ? (msg as any).contracts_remaining : null,
            option: (msg as any).option ?? null,
            option_symbol: (msg as any).option_symbol ?? null,
          }
        }
      } else if (msg.type === "position") {
        if (msg.symbol === symbol) {
          const res = msg.result as any
          const d = res.decision
          const last = barsRef.current.length ? barsRef.current[barsRef.current.length - 1] : null
          const lastPx = typeof last?.c === "number" ? last.c : null
          const summaryParts = [`POSITION_MGMT: ${d.action}`, d.reasoning]
          summaryParts.push(`underlying_symbol=${symbol}`)
          if (typeof lastStreamStateRef.current.contracts_remaining === "number") {
            summaryParts.push(`contracts=${lastStreamStateRef.current.contracts_remaining}`)
          }
          const opt = lastStreamStateRef.current.option
          if (opt) {
            const right = String((opt as any)?.right ?? "").toUpperCase()
            const exp = String((opt as any)?.expiration ?? "")
            const strike = (opt as any)?.strike
            const strikeStr = typeof strike === "number" ? String(strike) : ""
            const optLine = [right, exp, strikeStr].filter(Boolean).join(" ")
            if (optLine) summaryParts.push(`option=${optLine}`)
            const r = String((opt as any)?.right ?? "").toLowerCase()
            if (r === "call") summaryParts.push("direction=long")
            else if (r === "put") summaryParts.push("direction=short")
          }
          const optSym = res?.option_symbol ?? lastStreamStateRef.current.option_symbol ?? null
          if (optSym) summaryParts.push(`option_symbol=${optSym}`)
          summaryParts.push(`underlying_price=${lastPx ?? "N/A"}`)
          const optPx = res?.position_option_quote?.asof_price
          summaryParts.push(`option_price=${optPx ?? "N/A"}`)
          if (d.exit?.contracts_to_close) summaryParts.push(`contracts=${d.exit.contracts_to_close}`)
          if (d.adjustments?.new_stop_loss_premium != null) summaryParts.push(`stop_loss=${d.adjustments.new_stop_loss_premium}`)
          if (d.adjustments?.new_take_profit_premium != null) summaryParts.push(`take_profit=${d.adjustments.new_take_profit_premium}`)
          if (d.adjustments?.new_time_stop_minutes != null) summaryParts.push(`time_stop_minutes=${d.adjustments.new_time_stop_minutes}`)
          setAiMessages((prev) => [
            ...prev,
            {
              role: "ai",
              content: summaryParts.join("\n"),
              time: formatPSTFromRFC3339(res?.timestamp ?? res?.bar_time ?? new Date().toISOString()),
            },
          ])
        }
      }
    }

    return () => {
      intentionalCloseRef.current = true
      ws.close()
    }
  }, [applyMarkersToBars, baseWs, isOffHoursReadOnly, market?.session, recordAnalysisMarker, symbol])

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

  const chartPrevClose = isOffHoursReadOnly ? prevSession?.open : prevClose

  return (
    <TickerConsole
      symbol={symbol}
      bars={bars}
      prevClose={chartPrevClose}
      chartStatus={wsStatus === "open" ? "hot" : "normal"}
      aiMessages={aiMessages}
      headerLeft={
        <div className="flex items-center gap-4">
          <Link href="/tracking" className="rounded-xl bg-white/5 px-4 py-2 text-sm font-bold text-white/70 ring-1 ring-white/10 hover:bg-white/10 hover:text-white">
            ← Back
          </Link>
          <div className="flex items-baseline gap-3 min-w-0">
            <div className="text-2xl font-black tracking-tight">{symbol}</div>
            {typeof headerDisplayPrice === "number" && <div className="text-sm font-mono text-white/80">{headerDisplayPrice.toFixed(2)}</div>}
            {typeof headerDisplayPct === "number" && (
              <div className={cn("text-xs font-bold", headerDisplayPct >= 0 ? "text-emerald-400" : "text-red-400")}>
                {headerDisplayPct >= 0 ? "+" : ""}
                {headerDisplayPct.toFixed(2)}%
              </div>
            )}
          </div>

          {market && (
            <div className={cn("flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold ring-1", marketPillClass(market.session))}>
              <span className={cn("h-2 w-2 rounded-full", market.session === "regular" ? "bg-emerald-400" : market.session === "closed" ? "bg-white/30" : "bg-cyan-400")} />
              {marketLabel(market.session)}
            </div>
          )}

          {extTag && <div className="rounded-full bg-white/5 px-3 py-1 text-xs font-black text-white/60 ring-1 ring-white/10">{extTag}</div>}

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
      }
    />
  )
}
