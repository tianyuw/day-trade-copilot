"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import { CandleCard } from "../../components/CandleCard"
import { AICopilot, type ChatMessage } from "../../components/AICopilot"

type Direction = "long" | "short"
type OptionRight = "call" | "put"
type WatchCondition = { trigger_price: number; direction: "above" | "below"; expiry_minutes: number }
type TradePlan = {
  trade_id: string
  direction: Direction
  option: { right: OptionRight; expiration: string; strike: number }
  contracts: number
  risk: { stop_loss_premium: number | null; time_stop_minutes: number | null }
  take_profit_premium: number | null
}
type AnalysisAction = "buy_long" | "buy_short" | "ignore" | "follow_up" | "check_when_condition_meet"
type AnalysisResult = {
  analysis_id: string
  timestamp: string
  symbol: string
  action: AnalysisAction
  confidence: number
  reasoning: string
  pattern_name?: string | null
  breakout_price?: number | null
  watch_condition?: WatchCondition | null
  trade_plan?: TradePlan | null
}

type PositionDecisionAction =
  | "hold"
  | "close_all"
  | "close_partial"
  | "tighten_stop"
  | "adjust_take_profit"
  | "update_time_stop"

type PositionManagementResponse = {
  trade_id: string
  analysis_id: string
  timestamp: string
  symbol: string
  bar_time: string
  decision: {
    action: PositionDecisionAction
    reasoning: string
    exit?: { contracts_to_close?: number | null } | null
    adjustments?: {
      new_stop_loss_premium?: number | null
      new_take_profit_premium?: number | null
      new_time_stop_minutes?: number | null
    } | null
  }
}

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

const DEFAULT_SYMBOLS = ["META", "NVDA", "TSM", "PLTR", "AAPL", "NFLX", "SPY", "QQQ"]

function toRFC3339FromPSTInput(v: string): string | null {
  if (!v) return null
  const [datePart, timePart] = v.split("T")
  if (!datePart || !timePart) return null
  const [year, month, day] = datePart.split("-").map(Number)
  const [hour, minute] = timePart.split(":").map(Number)
  const d = new Date(Date.UTC(year, month - 1, day, hour + 8, minute))
  if (Number.isNaN(d.getTime())) return null
  return d.toISOString()
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

function formatPSTFromRFC3339(rfc3339: string): string {
  if (!rfc3339) return ""
  return formatPSTFromUtcSeconds(toEpochSeconds(rfc3339))
}

function AICopilotPanel({ symbol, messages }: { symbol: string; messages: ChatMessage[] }) {
  return <AICopilot symbol={symbol} messages={messages} />
}

type TradeStateName = "SCAN" | "FOLLOW_UP_PENDING" | "WATCH_PENDING" | "IN_POSITION"
type ActiveTrade = {
  trade_id: string
  direction: Direction
  option: { right: OptionRight; expiration: string; strike: number }
  option_symbol: string | null
  contracts_total: number
  contracts_remaining: number
  entry_time: string
  entry_premium: number | null
  risk: { stop_loss_premium: number | null; take_profit_premium: number | null; time_stop_minutes: number | null }
}
type PendingFollowUp = { armed: boolean }
type PendingWatch = { watch: WatchCondition; created_at_epoch_s: number; expires_at_epoch_s: number }

export default function DashboardPage() {
  const search = useSearchParams()
  const [selectedSymbol, setSelectedSymbol] = useState("NVDA")
  const [startLocal, setStartLocal] = useState("2026-01-09T06:31")
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackCursor, setPlaybackCursor] = useState(0)
  const [wsToken, setWsToken] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [resetToken, setResetToken] = useState(0)
  const [prevClose, setPrevClose] = useState<number | null>(null)

  const [bars, setBars] = useState<any[]>([])
  
  // AI State
  const [aiMessages, setAiMessages] = useState<ChatMessage[]>([])

  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const playbackCursorRef = useRef(0)
  const barsRef = useRef<any[]>([])
  const isPlayingRef = useRef(false)
  const userPausedRef = useRef(false)
  const autoPausedRef = useRef(false)
  const queuedMessagesRef = useRef<StreamMessage[]>([])
  const drainInProgressRef = useRef(false)

  const fsmRef = useRef<{
    state: TradeStateName
    followUp: PendingFollowUp
    watches: PendingWatch[]
    trade: ActiveTrade | null
    lastBarTime: string | null
    manageInflight: boolean
  }>({
    state: "SCAN",
    followUp: { armed: false },
    watches: [],
    trade: null,
    lastBarTime: null,
    manageInflight: false,
  })

  const symbolOptions = useMemo(() => {
    const s = String(selectedSymbol || "").trim().toUpperCase()
    if (!s) return DEFAULT_SYMBOLS
    if (DEFAULT_SYMBOLS.includes(s)) return DEFAULT_SYMBOLS
    return [s, ...DEFAULT_SYMBOLS]
  }, [selectedSymbol])

  useEffect(() => {
    const q = String(search.get("symbol") || "").trim().toUpperCase()
    if (!q) return
    if (q === selectedSymbol) return
    setSelectedSymbol(q)
  }, [search, selectedSymbol])

  // Reset AI messages on symbol change or reset
  useEffect(() => {
    fsmRef.current = {
      state: "SCAN",
      followUp: { armed: false },
      watches: [],
      trade: null,
      lastBarTime: null,
      manageInflight: false,
    }
    barsRef.current = []
    setAiMessages([
      {
        role: "system",
        content: `AI Copilot initialized for ${selectedSymbol}. Monitoring price action...`,
        time: formatPSTFromRFC3339(new Date().toISOString()),
      },
    ])
  }, [selectedSymbol, resetToken])

  useEffect(() => {
    isPlayingRef.current = isPlaying
  }, [isPlaying])

  const getBackendBase = () => {
    return (
      process.env.NEXT_PUBLIC_BACKEND_API ??
      `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
    )
  }

  const appendSystem = (text: string, timeIso?: string) => {
    setAiMessages((prev) => [
      ...prev,
      {
        role: "system",
        content: text,
        time: formatPSTFromRFC3339(timeIso ?? new Date().toISOString()),
      },
    ])
  }

  const appendAIAnalysis = (data: AnalysisResult, timeIso?: string) => {
    setAiMessages((prev) => [
      ...prev,
      {
        role: "ai",
        content: data,
        time: formatPSTFromRFC3339(timeIso ?? data?.timestamp ?? new Date().toISOString()),
        type: "analysis",
      },
    ])
  }

  const appendAIText = (text: string, timeIso?: string) => {
    setAiMessages((prev) => [
      ...prev,
      {
        role: "ai",
        content: text,
        time: formatPSTFromRFC3339(timeIso ?? new Date().toISOString()),
      },
    ])
  }

  const attachEntryToAnalysis = (analysisId: string, entry: { option_symbol: string | null }) => {
    if (!analysisId) return
    setAiMessages((prev) =>
      prev.map((m) => {
        if (m.role !== "ai" || m.type !== "analysis" || typeof m.content !== "object" || m.content == null) return m
        const c: any = m.content as any
        if (String(c?.analysis_id ?? "") !== analysisId) return m
        return { ...m, content: { ...c, entry } }
      }),
    )
  }

  const applyBarUIMarker = (timeIso: string, marker: { kind: "follow_up" | "watch"; color: "green" | "red" }) => {
    const last = barsRef.current[barsRef.current.length - 1]
    if (!last) return
    if (String(last?.t ?? "") !== timeIso) return
    barsRef.current = [
      ...barsRef.current.slice(0, -1),
      { ...last, ui_marker: marker },
    ]
    setBars(barsRef.current)
  }

  const drainQueuedMessages = async (processMessage: (m: StreamMessage) => Promise<void>) => {
    if (drainInProgressRef.current) return
    drainInProgressRef.current = true
    try {
      while (
        isPlayingRef.current &&
        !autoPausedRef.current &&
        queuedMessagesRef.current.length > 0
      ) {
        const next = queuedMessagesRef.current.shift()
        if (!next) continue
        await processMessage(next)
      }
    } finally {
      drainInProgressRef.current = false
    }
  }

  const runLLMBlocking = async (fn: () => Promise<void>, processMessage: (m: StreamMessage) => Promise<void>) => {
    if (!isPlayingRef.current) {
      await fn()
      return
    }
    autoPausedRef.current = true
    try {
      await fn()
    } finally {
      autoPausedRef.current = false
      await drainQueuedMessages(processMessage)
    }
  }

  const resolveOptionSymbol = async (plan: TradePlan): Promise<string | null> => {
    const base = getBackendBase()
    const exp = plan.option.expiration
    const res = await fetch(
      `${base}/api/options/contracts?underlying=${encodeURIComponent(selectedSymbol)}&expiration_date_gte=${encodeURIComponent(
        exp,
      )}&expiration_date_lte=${encodeURIComponent(exp)}&limit=1000`,
    )
    if (!res.ok) return null
    const payload = await res.json()
    const contracts: any[] = payload?.option_contracts ?? []
    const targetType = plan.option.right
    const targetStrike = Number(plan.option.strike)
    for (const c of contracts) {
      const type = String(c?.type ?? "").toLowerCase()
      const expDate = String(c?.expiration_date ?? "")
      const strike = Number(c?.strike_price)
      if (type !== targetType) continue
      if (expDate !== exp) continue
      if (Number.isFinite(strike) && Math.abs(strike - targetStrike) > 1e-6) continue
      const sym = String(c?.symbol ?? "").toUpperCase()
      if (sym) return sym
    }
    return null
  }

  const enterPositionFromPlan = async (analysis: AnalysisResult) => {
    const plan = analysis.trade_plan
    if (!plan) return
    const optionSymbol: string | null = null

    const trade: ActiveTrade = {
      trade_id: plan.trade_id,
      direction: plan.direction,
      option: plan.option,
      option_symbol: optionSymbol,
      contracts_total: plan.contracts,
      contracts_remaining: plan.contracts,
      entry_time: analysis.timestamp,
      entry_premium: null,
      risk: {
        stop_loss_premium: plan.risk?.stop_loss_premium ?? null,
        take_profit_premium: plan.take_profit_premium ?? null,
        time_stop_minutes: plan.risk?.time_stop_minutes ?? null,
      },
    }

    fsmRef.current.trade = trade
    fsmRef.current.state = "IN_POSITION"
    fsmRef.current.followUp = { armed: false }
    fsmRef.current.watches = []
    attachEntryToAnalysis(analysis.analysis_id, { option_symbol: optionSymbol })

    void (async () => {
      try {
        const resolved = await resolveOptionSymbol(plan)
        trade.option_symbol = resolved
        attachEntryToAnalysis(analysis.analysis_id, { option_symbol: resolved })
      } catch {
        trade.option_symbol = null
      }
    })()
  }

  const handleAIResultForFSM = async (analysis: AnalysisResult) => {
    if (fsmRef.current.state === "IN_POSITION") return
    const action = analysis.action
    if (action === "follow_up") {
      fsmRef.current.state = "FOLLOW_UP_PENDING"
      fsmRef.current.followUp = { armed: true }
      fsmRef.current.watches = []
      return
    }
    if (action === "check_when_condition_meet" && analysis.watch_condition) {
      const nowEpoch = toEpochSeconds(analysis.timestamp)
      const expires = nowEpoch + analysis.watch_condition.expiry_minutes * 60
      const next: PendingWatch = {
        watch: analysis.watch_condition,
        created_at_epoch_s: nowEpoch,
        expires_at_epoch_s: expires,
      }
      fsmRef.current.watches = [...fsmRef.current.watches, next]
      fsmRef.current.followUp = { armed: false }
      return
    }
    if ((action === "buy_long" || action === "buy_short") && analysis.trade_plan) {
      await enterPositionFromPlan(analysis)
      return
    }

    fsmRef.current.state = "SCAN"
    fsmRef.current.followUp = { armed: false }
    fsmRef.current.watches = []
  }

  const requestAnalyze = async (timeIso: string) => {
      try {
          const base = getBackendBase()
          const res = await fetch(`${base}/api/analyze`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                  symbol: selectedSymbol,
                  current_time: timeIso
              })
          })
          
          if (!res.ok) throw new Error("Analysis failed")
          
          const data = (await res.json()) as AnalysisResult
          appendAIAnalysis(data, data?.timestamp ?? timeIso)
          await handleAIResultForFSM(data)
          
      } catch (e) {
          console.error(e)
          appendSystem(`Analysis Error: ${e instanceof Error ? e.message : 'Unknown error'}`, new Date().toISOString())
      }
  }

  const requestPositionManage = async (barTimeIso: string) => {
    const trade = fsmRef.current.trade
    if (!trade) return
    if (fsmRef.current.manageInflight) return
    fsmRef.current.manageInflight = true
    try {
      const base = getBackendBase()
      const ohlcv = barsRef.current.slice(-300).map((b) => ({
        t: b.t,
        open: b.o,
        high: b.h,
        low: b.l,
        close: b.c,
        volume: b.v,
      }))
      const res = await fetch(`${base}/api/ai/position_manage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          trade_id: trade.trade_id,
          symbol: selectedSymbol,
          bar_time: barTimeIso,
          position: {
            direction: trade.direction,
            option: trade.option,
            contracts_total: trade.contracts_total,
            contracts_remaining: trade.contracts_remaining,
            entry: { time: trade.entry_time, premium: trade.entry_premium },
            risk: trade.risk,
          },
          option_symbol: trade.option_symbol,
          ohlcv_1m: ohlcv,
        }),
      })
      if (!res.ok) throw new Error("Position manage failed")
      const data = (await res.json()) as PositionManagementResponse

      const d = data.decision
      const summaryParts = [`POSITION_MGMT: ${d.action}`, d.reasoning]
      const lastBar = barsRef.current[barsRef.current.length - 1]
      const lastPx = typeof lastBar?.c === "number" ? lastBar.c : null
      summaryParts.push(`last_px=${lastPx ?? "N/A"}`)
      summaryParts.push(`contracts=${trade.contracts_remaining}/${trade.contracts_total}`)
      summaryParts.push(`direction=${trade.direction}`)
      summaryParts.push(`option=${trade.option.right} ${trade.option.expiration} ${trade.option.strike}`)
      summaryParts.push(`option_symbol=${trade.option_symbol ?? "N/A"}`)
      summaryParts.push(`stop_loss_premium=${trade.risk.stop_loss_premium ?? "N/A"}`)
      summaryParts.push(`take_profit_premium=${trade.risk.take_profit_premium ?? "N/A"}`)
      summaryParts.push(`time_stop_minutes=${trade.risk.time_stop_minutes ?? "N/A"}`)
      if (d.exit?.contracts_to_close) summaryParts.push(`contracts_to_close=${d.exit.contracts_to_close}`)
      if (d.adjustments?.new_stop_loss_premium != null) summaryParts.push(`new_stop=${d.adjustments.new_stop_loss_premium}`)
      if (d.adjustments?.new_take_profit_premium != null) summaryParts.push(`new_tp=${d.adjustments.new_take_profit_premium}`)
      if (d.adjustments?.new_time_stop_minutes != null) summaryParts.push(`new_time_stop=${d.adjustments.new_time_stop_minutes}`)
      appendAIText(summaryParts.join("\n"), data.timestamp ?? barTimeIso)

      if (d.action === "close_all") {
        trade.contracts_remaining = 0
      } else if (d.action === "close_partial") {
        const n = d.exit?.contracts_to_close ?? 0
        trade.contracts_remaining = Math.max(0, trade.contracts_remaining - Math.max(0, n))
      } else if (d.action === "tighten_stop") {
        if (d.adjustments?.new_stop_loss_premium != null) trade.risk.stop_loss_premium = d.adjustments.new_stop_loss_premium
      } else if (d.action === "adjust_take_profit") {
        if (d.adjustments?.new_take_profit_premium != null) trade.risk.take_profit_premium = d.adjustments.new_take_profit_premium
      } else if (d.action === "update_time_stop") {
        if (d.adjustments?.new_time_stop_minutes != null) trade.risk.time_stop_minutes = d.adjustments.new_time_stop_minutes
      }

      if (trade.contracts_remaining === 0) {
        fsmRef.current.state = "SCAN"
        fsmRef.current.trade = null
        fsmRef.current.followUp = { armed: false }
        fsmRef.current.watches = []
      }
    } catch (e) {
      console.error(e)
      appendSystem(`Position Mgmt Error: ${e instanceof Error ? e.message : "Unknown error"}`, barTimeIso)
    } finally {
      fsmRef.current.manageInflight = false
    }
  }

  const startRFC = useMemo(() => toRFC3339FromPSTInput(startLocal), [startLocal])

  useEffect(() => {
    async function fetchPrevClose() {
      try {
        const base =
          process.env.NEXT_PUBLIC_BACKEND_API ??
          `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
        const res = await fetch(`${base}/api/stocks/prev_close?symbols=${selectedSymbol}&asof=${startRFC}`)
        if (!res.ok) throw new Error("Failed to fetch prev close")
        const data = await res.json()
        setPrevClose(data.prev_close?.[selectedSymbol] ?? null)
      } catch (e) {
        console.error(e)
        setPrevClose(null)
      }
    }
    if (startRFC) fetchPrevClose()
  }, [selectedSymbol, startRFC])

  useEffect(() => {
    intentionalCloseRef.current = true
    wsRef.current?.close()
    wsRef.current = null

    if (!isPlaying) return

    intentionalCloseRef.current = false
    setError(null)

    const base =
      process.env.NEXT_PUBLIC_BACKEND_WS ??
      `ws://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_WS_PORT ?? "8000"}`
    const url = `${base}/ws/playback?symbols=${encodeURIComponent(selectedSymbol)}&start=${encodeURIComponent(
      startRFC ?? "",
    )}&speed=1&cursor=${encodeURIComponent(String(playbackCursorRef.current))}`

    const ws = new WebSocket(url)
    wsRef.current = ws

    const processMessage = async (msg: StreamMessage) => {
      if (msg.type === "init") {
        if (typeof msg.cursor === "number") {
          playbackCursorRef.current = msg.cursor
          setPlaybackCursor(msg.cursor)
        }
        if (msg.symbol === selectedSymbol) {
          barsRef.current = msg.bars || []
          setBars(barsRef.current)
        }

        if (msg.bars && msg.bars.length > 0) {
          const firstBar = msg.bars[msg.bars.length - 1]
          if (firstBar && firstBar.t) {
            const barTime = new Date(firstBar.t).getTime()
            const userTime = new Date(startLocal).getTime()
            if (Math.abs(barTime - userTime) > 24 * 60 * 60 * 1000) {
              setError(`No data at exact time. Jumped to nearest: ${new Date(firstBar.t).toLocaleString()}`)
            }
          }
        }
        return
      }

      if (msg.type === "bar") {
        if (typeof msg.i === "number") {
          playbackCursorRef.current = msg.i + 1
          setPlaybackCursor(msg.i + 1)
        }
        if (msg.symbol === selectedSymbol) {
          barsRef.current = [...barsRef.current, msg.bar].slice(-1000)
          setBars(barsRef.current)
          const barTimeIso = String(msg.bar?.t ?? "")
          const hasQuantSignal = Boolean(msg.bar?.indicators?.signal)
          fsmRef.current.lastBarTime = barTimeIso || null

          if (fsmRef.current.state === "IN_POSITION" && barTimeIso) {
            await runLLMBlocking(() => requestPositionManage(barTimeIso), processMessage)
            return
          }

          if (barTimeIso && fsmRef.current.watches.length > 0) {
            const nowEpoch = toEpochSeconds(barTimeIso)
            const active = fsmRef.current.watches.filter((w) => nowEpoch < w.expires_at_epoch_s)
            if (active.length !== fsmRef.current.watches.length) {
              fsmRef.current.watches = active
            }

            if (active.length > 0) {
              const closePx = Number(msg.bar?.c)
              const hitWatches = active
                .filter((w) => {
                  const cond = w.watch
                  if (!cond) return false
                  return cond.direction === "above" ? closePx >= cond.trigger_price : closePx <= cond.trigger_price
                })
                .sort((a, b) => a.created_at_epoch_s - b.created_at_epoch_s)

              if (hitWatches.length > 0) {
                const primary = hitWatches[0]
                const primaryColor: "green" | "red" = primary.watch.direction === "above" ? "green" : "red"
                applyBarUIMarker(barTimeIso, { kind: "watch", color: primaryColor })
                fsmRef.current.watches = active.filter((w) => !hitWatches.includes(w))
                await runLLMBlocking(() => requestAnalyze(barTimeIso), processMessage)
                return
              }
            }
          }

          if (fsmRef.current.state === "FOLLOW_UP_PENDING" && fsmRef.current.followUp.armed && barTimeIso) {
            if (!hasQuantSignal) {
              fsmRef.current.followUp = { armed: false }
              const up = Number(msg.bar?.c) >= Number(msg.bar?.o)
              applyBarUIMarker(barTimeIso, { kind: "follow_up", color: up ? "green" : "red" })
              await runLLMBlocking(() => requestAnalyze(barTimeIso), processMessage)
            }
            return
          }
        }
        return
      }

      if (msg.type === "analysis") {
        if (msg.symbol === selectedSymbol) {
          if (fsmRef.current.state === "IN_POSITION") return
          const data = msg.result as AnalysisResult
          appendAIAnalysis(data, data?.timestamp ?? new Date().toISOString())
          void handleAIResultForFSM(data)
        }
        return
      }

      if (msg.type === "done") {
        queuedMessagesRef.current = []
        autoPausedRef.current = false
        setIsPlaying(false)
      }
    }

    ws.onmessage = async (ev) => {
      let msg: StreamMessage
      try {
        msg = JSON.parse(ev.data)
      } catch { return }

      if (!isPlayingRef.current) return

      if (msg.type === "error") {
        setError(msg.message)
        queuedMessagesRef.current = []
        autoPausedRef.current = false
        setIsPlaying(false)
        return
      }

      if (autoPausedRef.current) {
        queuedMessagesRef.current.push(msg)
        if (queuedMessagesRef.current.length > 5000) {
          setError("Replay paused too long; buffered messages exceeded limit")
          queuedMessagesRef.current = []
          autoPausedRef.current = false
          setIsPlaying(false)
        }
        return
      }

      await processMessage(msg)
      await drainQueuedMessages(processMessage)
    }

    ws.onerror = () => {
      if (!intentionalCloseRef.current) setError("Connection failed")
    }
    
    ws.onclose = () => {
      if (!intentionalCloseRef.current && isPlaying) {
        setError("Connection closed unexpectedly")
        setIsPlaying(false)
      }
    }

    return () => {
      intentionalCloseRef.current = true
      ws.close()
    }
  }, [isPlaying, selectedSymbol, startRFC, wsToken])

  // Reset handler
  const handleReset = () => {
    setIsPlaying(false)
    setBars([])
    playbackCursorRef.current = 0
    setPlaybackCursor(0)
    setError(null)
    setResetToken(prev => prev + 1)
  }

  // Symbol Change Handler
  const handleSymbolChange = (sym: string) => {
    if (sym === selectedSymbol) return
    setSelectedSymbol(sym)
    handleReset()
  }

  return (
    <main className="flex h-screen flex-col bg-neon-radial text-white font-sans overflow-hidden">

      {/* Top Control Bar */}
      <div className="flex-none border-b border-white/10 bg-black/20 backdrop-blur-xl px-6 py-4">
        <div className="mx-auto flex max-w-[1600px] flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          
          {/* Left: Ticker & Status */}
          <div className="flex items-center gap-6">
             <div className="relative">
                <select 
                  value={selectedSymbol}
                  onChange={(e) => handleSymbolChange(e.target.value)}
                  className="appearance-none rounded-xl bg-white/10 pl-4 pr-10 py-2.5 text-sm font-bold text-white hover:bg-white/15 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-colors cursor-pointer"
                >
                  {symbolOptions.map(s => <option key={s} value={s} className="bg-slate-900">{s}</option>)}
                </select>
                <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-white/50">
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
             </div>

             <div className="h-8 w-px bg-white/10 hidden lg:block" />

             <div className="flex items-center gap-3">
               <div className="text-xs font-medium text-white/50 uppercase tracking-wider">Status</div>
               {isPlaying ? (
                 <div className="flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-bold text-emerald-400 ring-1 ring-emerald-500/20">
                   <span className="relative flex h-2 w-2">
                     <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                     <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                   </span>
                   LIVE REPLAY
                 </div>
               ) : (
                 <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-xs font-bold text-white/40 ring-1 ring-white/10">
                   <div className="h-2 w-2 rounded-full bg-white/20" />
                   PAUSED
                 </div>
               )}
             </div>
          </div>

          {/* Right: Controls */}
          <div className="flex flex-wrap items-center gap-4">
             {/* Time Selector */}
             <div className="flex items-center gap-3 rounded-xl bg-black/40 px-4 py-2 ring-1 ring-white/10">
               <span className="text-xs font-bold text-white/40 uppercase">Start Time (PST)</span>
               <input
                 type="datetime-local"
                 value={startLocal}
                 onChange={(e) => {
                   setStartLocal(e.target.value)
                   handleReset()
                 }}
                 className="bg-transparent text-sm font-mono font-medium text-white outline-none focus:text-cyan-300 [&::-webkit-calendar-picker-indicator]:invert [&::-webkit-calendar-picker-indicator]:opacity-50 hover:[&::-webkit-calendar-picker-indicator]:opacity-100"
               />
             </div>

             {/* Action Buttons */}
             <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const next = !isPlaying
                    userPausedRef.current = !next
                    setIsPlaying(next)
                  }}
                  className={`flex items-center gap-2 rounded-xl px-6 py-2.5 text-sm font-bold transition-all ${
                    isPlaying 
                      ? "bg-amber-500/20 text-amber-300 ring-1 ring-amber-500/50 hover:bg-amber-500/30" 
                      : "bg-white text-black hover:bg-cyan-50 hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]"
                  }`}
                >
                  {isPlaying ? (
                    <>
                      <svg className="h-4 w-4 fill-current" viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg>
                      Pause
                    </>
                  ) : (
                    <>
                      <svg className="h-4 w-4 fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                      Start Replay
                    </>
                  )}
                </button>

                <button
                  onClick={handleReset}
                  className="rounded-xl bg-white/5 p-2.5 text-white/70 ring-1 ring-white/10 hover:bg-white/10 hover:text-white transition-colors"
                  title="Reset"
                >
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
             </div>
          </div>

        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex-1 overflow-hidden p-6">
        <div className="mx-auto flex h-full max-w-[1600px] gap-6">
          
          {/* Left: Market View (Chart) */}
          <div className="flex-[2] min-w-0 flex flex-col gap-4">
             {/* Chart Container */}
             <div className="relative flex-1 rounded-3xl bg-black/40 shadow-neo ring-1 ring-white/10 backdrop-blur-md overflow-hidden p-1">
                <CandleCard 
                   symbol={selectedSymbol} 
                   bars={bars} 
                   prevClose={prevClose}
                   className="h-full w-full !bg-transparent !shadow-none !ring-0 !backdrop-blur-none" 
                   status={isPlaying ? "hot" : "normal"}
                   onAnalyze={requestAnalyze}
                />
                
                {/* Overlay Info (optional) */}
                
             </div>
             
             {/* Error Toast */}
             {error && (
               <div className="rounded-xl bg-red-500/10 px-4 py-3 text-sm font-medium text-red-200 ring-1 ring-red-500/20 flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2">
                 <svg className="h-5 w-5 flex-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                 </svg>
                 {error}
               </div>
             )}
          </div>

          {/* Right: AI Copilot */}
          <div className="flex-1 min-w-[320px] hidden lg:block">
            <AICopilotPanel symbol={selectedSymbol} messages={aiMessages} />
          </div>

        </div>
      </div>
    </main>
  )
}
