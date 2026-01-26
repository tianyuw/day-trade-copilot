"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import type { ChatMessage } from "../../components/AICopilot"
import { TickerConsole } from "../../components/TickerConsole"
import { TransportControls } from "../../components/TransportControls"
import { useBackendBaseUrls } from "../../components/hooks/useBackendBaseUrls"
import { usePrevClose } from "../../components/hooks/usePrevClose"

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
  option_symbol?: string | null
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
  option_symbol?: string | null
}

type StreamInit = {
  type: "init"
  mode: "realtime" | "playback"
  symbol: string
  bars: any[]
  cursor?: number
}
type StreamBar = { type: "bar"; mode: "realtime" | "playback"; symbol: string; analysis_trigger_reason?: any; bar: any; i?: number }
type StreamAnalysis = { type: "analysis"; mode: "realtime" | "playback"; symbol: string; trigger_reason?: any; result: any }
type StreamState = {
  type: "state"
  mode: "realtime" | "playback"
  symbol: string
  state: string
  in_position: boolean
  contracts_total?: number | null
  contracts_remaining?: number | null
  trade_id?: string | null
  option?: any | null
  option_symbol?: string | null
}
type StreamPosition = { type: "position"; mode: "realtime" | "playback"; symbol: string; trigger_reason?: any; result: any }
type StreamDone = { type: "done"; mode: "realtime" | "playback"; cursor?: number }
type StreamError = { type: "error"; message: string }
type StreamMessage = StreamInit | StreamBar | StreamAnalysis | StreamState | StreamPosition | StreamDone | StreamError

const DEFAULT_SYMBOLS = ["META", "NVDA", "TSM", "PLTR", "AAPL", "NFLX", "SPY", "QQQ"]

const PT_TIME_ZONE = "America/Los_Angeles"
const ptTimeFormatter = new Intl.DateTimeFormat("en-US", {
  timeZone: PT_TIME_ZONE,
  hour: "2-digit",
  minute: "2-digit",
  hour12: false,
})

function getTimeZoneOffsetMs(timeZone: string, date: Date): number {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date)
  const m: Record<string, string> = {}
  for (const p of parts) {
    if (p.type !== "literal") m[p.type] = p.value
  }
  const asUtc = Date.UTC(
    Number(m.year),
    Number(m.month) - 1,
    Number(m.day),
    Number(m.hour),
    Number(m.minute),
    Number(m.second),
  )
  return asUtc - date.getTime()
}

function toRFC3339FromPTInput(v: string): string | null {
  if (!v) return null
  const [datePart, timePart] = v.split("T")
  if (!datePart || !timePart) return null
  const [year, month, day] = datePart.split("-").map(Number)
  const [hour, minute] = timePart.split(":").map(Number)
  const utcApprox = Date.UTC(year, month - 1, day, hour, minute, 0)
  if (Number.isNaN(utcApprox)) return null

  const offset1 = getTimeZoneOffsetMs(PT_TIME_ZONE, new Date(utcApprox))
  let utcMs = utcApprox - offset1
  const offset2 = getTimeZoneOffsetMs(PT_TIME_ZONE, new Date(utcMs))
  if (offset2 !== offset1) utcMs = utcApprox - offset2
  const d = new Date(utcMs)
  if (Number.isNaN(d.getTime())) return null
  return d.toISOString()
}

const toRFC3339FromPSTInput = toRFC3339FromPTInput

function toEpochSeconds(rfc3339: string): number {
  return Math.floor(new Date(rfc3339).getTime() / 1000)
}

function formatPTFromUtcSeconds(utcSeconds: number): string {
  return ptTimeFormatter.format(new Date(utcSeconds * 1000))
}

function formatPTFromRFC3339(rfc3339: string): string {
  if (!rfc3339) return ""
  return formatPTFromUtcSeconds(toEpochSeconds(rfc3339))
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
  const { baseHttp, baseWs } = useBackendBaseUrls()
  const [selectedSymbol, setSelectedSymbol] = useState("NVDA")
  const [startLocal, setStartLocal] = useState("2026-01-09T06:31")
  const playbackFlow: "ack" = "ack"
  const playbackPaceMs = 1000
  const playbackSpeedSeconds = 1.0
  const [isPlaying, setIsPlaying] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [resetToken, setResetToken] = useState(0)

  const [bars, setBars] = useState<any[]>([])
  
  // AI State
  const [aiMessages, setAiMessages] = useState<ChatMessage[]>([])
  const [backendState, setBackendState] = useState<string>("SCAN")
  const [backendInPosition, setBackendInPosition] = useState(false)
  const [backendContracts, setBackendContracts] = useState<{ remaining: number | null; total: number | null }>({
    remaining: null,
    total: null,
  })

  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const playbackCursorRef = useRef(0)
  const barsRef = useRef<any[]>([])
  const isPlayingRef = useRef(false)
  const lastBackendStateRef = useRef("SCAN")
  const userPausedRef = useRef(false)
  const autoPausedRef = useRef(false)
  const ackTimeoutRef = useRef<number | null>(null)
  const queuedMessagesRef = useRef<StreamMessage[]>([])
  const drainInProgressRef = useRef(false)
  const replaySessionIdRef = useRef(0)
  const inflightFetchControllersRef = useRef<Set<AbortController>>(new Set())

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
  const lastStreamStateRef = useRef<{
    contracts_remaining: number | null
    option: StreamState["option"] | null
    option_symbol: string | null
  }>({ contracts_remaining: null, option: null, option_symbol: null })

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
    lastStreamStateRef.current = { contracts_remaining: null, option: null, option_symbol: null }
    barsRef.current = []
    setBackendState("SCAN")
    setBackendInPosition(false)
    setBackendContracts({ remaining: null, total: null })
    lastBackendStateRef.current = "SCAN"
    setAiMessages([
      {
        role: "system",
        content: `AI Copilot initialized for ${selectedSymbol}. Monitoring price action...`,
        time: formatPTFromRFC3339(new Date().toISOString()),
      },
    ])
  }, [selectedSymbol, resetToken])

  useEffect(() => {
    isPlayingRef.current = isPlaying
  }, [isPlaying])

  const beginNewReplaySession = () => {
    replaySessionIdRef.current += 1
    return replaySessionIdRef.current
  }

  const abortAllInflightFetches = () => {
    const ctrls = Array.from(inflightFetchControllersRef.current)
    inflightFetchControllersRef.current.clear()
    for (const c of ctrls) {
      try { c.abort() } catch {}
    }
  }

  const stopReplay = () => {
    beginNewReplaySession()
    isPlayingRef.current = false
    intentionalCloseRef.current = true
    if (ackTimeoutRef.current != null) {
      try { window.clearTimeout(ackTimeoutRef.current) } catch {}
      ackTimeoutRef.current = null
    }
    try { wsRef.current?.close() } catch {}
    queuedMessagesRef.current = []
    autoPausedRef.current = false
    fsmRef.current.manageInflight = false
    abortAllInflightFetches()
    setIsPlaying(false)
  }

  const startReplay = () => {
    beginNewReplaySession()
    isPlayingRef.current = true
    setIsPlaying(true)
  }

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
        time: formatPTFromRFC3339(timeIso ?? new Date().toISOString()),
      },
    ])
  }

  const appendAIAnalysis = (
    data: AnalysisResult,
    timeIso?: string,
    trigger_reason?: "quant_signal" | "follow_up" | "watch_condition" | "position_management",
  ) => {
    setAiMessages((prev) => [
      ...prev,
      {
        role: "ai",
        content: data,
        time: formatPTFromRFC3339(timeIso ?? data?.timestamp ?? new Date().toISOString()),
        type: "analysis",
        trigger_reason,
      },
    ])
  }

  const appendAIText = (text: string, timeIso?: string) => {
    setAiMessages((prev) => [
      ...prev,
      {
        role: "ai",
        content: text,
        time: formatPTFromRFC3339(timeIso ?? new Date().toISOString()),
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
    void timeIso
  }

  const requestPositionManage = async (barTimeIso: string) => {
    void barTimeIso
  }

  const startRFC = useMemo(() => toRFC3339FromPTInput(startLocal), [startLocal])
  const { prevClose } = usePrevClose(baseHttp, selectedSymbol, { asof: startRFC, enabled: !!startRFC })

  useEffect(() => {
    intentionalCloseRef.current = true
    wsRef.current?.close()
    wsRef.current = null

    if (!isPlaying) return

    intentionalCloseRef.current = false
    setError(null)

    const url = `${baseWs}/ws/playback?symbols=${encodeURIComponent(selectedSymbol)}&start=${encodeURIComponent(
      startRFC ?? "",
    )}&speed=${encodeURIComponent(String(playbackSpeedSeconds))}&flow=${encodeURIComponent(playbackFlow)}&cursor=${encodeURIComponent(String(playbackCursorRef.current))}&analyze=true&analysis_window_minutes=300`

    const ws = new WebSocket(url)
    wsRef.current = ws

    const processMessage = async (msg: StreamMessage) => {
      if (msg.type === "init") {
        if (typeof msg.cursor === "number") {
          playbackCursorRef.current = msg.cursor
        }
        if (msg.symbol === selectedSymbol) {
          barsRef.current = msg.bars || []
          setBars(barsRef.current)
        }

        if (msg.bars && msg.bars.length > 0) {
          const firstBar = msg.bars[msg.bars.length - 1]
          if (firstBar && firstBar.t) {
            const barTime = new Date(firstBar.t).getTime()
            const desiredMs = startRFC ? new Date(startRFC).getTime() : null
            if (typeof desiredMs === "number" && Number.isFinite(desiredMs)) {
              const diffMs = Math.abs(barTime - desiredMs)
              if (diffMs > 2 * 60 * 1000) {
                const diffMin = Math.round(diffMs / (60 * 1000))
                setError(`No data at exact time. Started at ${new Date(firstBar.t).toLocaleString()} (Δ${diffMin}m)`)
              }
            }
          }
        }
        return
      }

      if (msg.type === "bar") {
        const ackI = typeof msg.i === "number" ? msg.i : null
        const nextCursor = ackI != null ? ackI + 1 : null
        try {
          if (msg.symbol === selectedSymbol) {
            const hasTrigger = Boolean((msg as any).analysis_trigger_reason)
            const o = typeof (msg as any)?.bar?.o === "number" ? (msg as any).bar.o : null
            const c = typeof (msg as any)?.bar?.c === "number" ? (msg as any).bar.c : null
            const color: "green" | "red" = typeof o === "number" && typeof c === "number" && c >= o ? "green" : "red"
            const nextBar = hasTrigger ? { ...(msg as any).bar, ui_marker: { kind: "analysis", color } } : msg.bar
            const last = barsRef.current[barsRef.current.length - 1]
            if (last && String(last?.t ?? "") === String(msg.bar?.t ?? "")) {
              barsRef.current = [...barsRef.current.slice(0, -1), nextBar].slice(-1000)
            } else {
              barsRef.current = [...barsRef.current, nextBar].slice(-1000)
            }
            const barTimeIso = String(msg.bar?.t ?? "")
            setBars(barsRef.current)
            fsmRef.current.lastBarTime = barTimeIso || null
          }
        } finally {
          if (nextCursor != null) {
            playbackCursorRef.current = nextCursor
          }
          if (ackI != null && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            if (ackTimeoutRef.current != null) {
              try { window.clearTimeout(ackTimeoutRef.current) } catch {}
              ackTimeoutRef.current = null
            }
            const sessionId = replaySessionIdRef.current
            const delayMs = Math.max(0, Math.round(playbackPaceMs))
            ackTimeoutRef.current = window.setTimeout(() => {
              if (
                isPlayingRef.current &&
                sessionId === replaySessionIdRef.current &&
                wsRef.current &&
                wsRef.current.readyState === WebSocket.OPEN
              ) {
                wsRef.current.send(JSON.stringify({ type: "ack", i: ackI }))
              }
            }, delayMs)
          }
        }
        return
      }

      if (msg.type === "analysis") {
        if (msg.symbol === selectedSymbol) {
          const data = msg.result as AnalysisResult
          appendAIAnalysis(
            data,
            data?.timestamp ?? new Date().toISOString(),
            (msg as any)?.trigger_reason as any,
          )
        }
        return
      }

      if (msg.type === "state") {
        if (msg.symbol === selectedSymbol) {
          setBackendInPosition(Boolean((msg as any).in_position))
          setBackendContracts({
            remaining: typeof (msg as any).contracts_remaining === "number" ? (msg as any).contracts_remaining : null,
            total: typeof (msg as any).contracts_total === "number" ? (msg as any).contracts_total : null,
          })
          lastStreamStateRef.current = {
            contracts_remaining: typeof (msg as any).contracts_remaining === "number" ? (msg as any).contracts_remaining : null,
            option: (msg as any).option ?? null,
            option_symbol: (msg as any).option_symbol ?? null,
          }
          const next = String((msg as any).state ?? "SCAN")
          setBackendState(next)
          if (lastBackendStateRef.current !== next) {
            lastBackendStateRef.current = next
            appendSystem(`STATE: ${next}`, new Date().toISOString())
          }
        }
        return
      }

      if (msg.type === "position") {
        if (msg.symbol === selectedSymbol) {
          const data = msg.result as PositionManagementResponse
          const d = data?.decision
          const summaryParts = [`POSITION_MGMT: ${d?.action ?? "unknown"}`, String(d?.reasoning ?? "")].filter(Boolean)
          const optionFromState = lastStreamStateRef.current.option ?? fsmRef.current.trade?.option ?? null
          const optionSymbolFromState =
            lastStreamStateRef.current.option_symbol ?? fsmRef.current.trade?.option_symbol ?? null
          const dirFromState = fsmRef.current.trade?.direction ?? null
          summaryParts.push(`underlying_symbol=${selectedSymbol}`)
          if (typeof lastStreamStateRef.current.contracts_remaining === "number") {
            summaryParts.push(`contracts=${lastStreamStateRef.current.contracts_remaining}`)
          }
          if (dirFromState) summaryParts.push(`direction=${dirFromState}`)
          if (optionFromState) {
            const right = String((optionFromState as any)?.right ?? "").toUpperCase()
            const exp = String((optionFromState as any)?.expiration ?? "")
            const strike = (optionFromState as any)?.strike
            const strikeStr = typeof strike === "number" ? String(strike) : ""
            const optLine = [right, exp, strikeStr].filter(Boolean).join(" ")
            if (optLine) summaryParts.push(`option=${optLine}`)
            if (!dirFromState && (optionFromState as any)?.right) {
              const r = String((optionFromState as any).right).toLowerCase()
              if (r === "call") summaryParts.push("direction=long")
              else if (r === "put") summaryParts.push("direction=short")
            }
          }
          const optionSymbolFromResponse = (data as any)?.option_symbol
          const optionSymbolFinal = optionSymbolFromResponse ?? optionSymbolFromState ?? null
          if (optionSymbolFinal) summaryParts.push(`option_symbol=${optionSymbolFinal}`)
          const lastBar = barsRef.current[barsRef.current.length - 1]
          const lastPx = typeof lastBar?.c === "number" ? lastBar.c : null
          summaryParts.push(`underlying_price=${lastPx ?? "N/A"}`)
          const optPx = (data as any)?.position_option_quote?.asof_price
          summaryParts.push(`option_price=${optPx ?? "N/A"}`)
          if (d?.exit?.contracts_to_close) summaryParts.push(`contracts=${d.exit.contracts_to_close}`)
          if (d?.adjustments?.new_stop_loss_premium != null) summaryParts.push(`stop_loss=${d.adjustments.new_stop_loss_premium}`)
          if (d?.adjustments?.new_take_profit_premium != null) summaryParts.push(`take_profit=${d.adjustments.new_take_profit_premium}`)
          if (d?.adjustments?.new_time_stop_minutes != null) summaryParts.push(`time_stop_minutes=${d.adjustments.new_time_stop_minutes}`)
          appendAIText(summaryParts.join("\n"), data?.timestamp ?? data?.bar_time ?? new Date().toISOString())
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
      if (ackTimeoutRef.current != null) {
        try { window.clearTimeout(ackTimeoutRef.current) } catch {}
        ackTimeoutRef.current = null
      }
      ws.close()
    }
  }, [isPlaying, selectedSymbol, startRFC, playbackFlow, playbackPaceMs, playbackSpeedSeconds, baseWs])

  // Reset handler
  const handleReset = () => {
    stopReplay()
    setBars([])
    playbackCursorRef.current = 0
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
    <TickerConsole
      symbol={selectedSymbol}
      bars={bars}
      prevClose={prevClose}
      chartStatus={isPlaying ? "hot" : "normal"}
      aiMessages={aiMessages}
      headerLeft={
        <div className="flex items-center gap-6">
          <div className="relative">
            <select
              value={selectedSymbol}
              onChange={(e) => handleSymbolChange(e.target.value)}
              className="appearance-none rounded-xl bg-white/10 pl-4 pr-10 py-2.5 text-sm font-bold text-white hover:bg-white/15 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 transition-colors cursor-pointer"
            >
              {symbolOptions.map((s) => (
                <option key={s} value={s} className="bg-slate-900">
                  {s}
                </option>
              ))}
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

          <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-xs font-bold text-white/70 ring-1 ring-white/10">
            <div className={`h-2 w-2 rounded-full ${backendInPosition ? "bg-emerald-400" : "bg-white/30"}`} />
            {backendState}
            {backendInPosition ? ` (${backendContracts.remaining ?? "?"}/${backendContracts.total ?? "?"})` : ""}
          </div>
        </div>
      }
      headerRight={
        <TransportControls
          mode="playback"
          startLocal={startLocal}
          onStartLocalChange={(v) => {
            setStartLocal(v)
            handleReset()
          }}
          isPlaying={isPlaying}
          onTogglePlay={() => {
            const next = !isPlaying
            userPausedRef.current = !next
            if (next) startReplay()
            else stopReplay()
          }}
          onReset={handleReset}
        />
      }
      notice={
        error ? (
          <div className="rounded-xl bg-red-500/10 px-4 py-3 text-sm font-medium text-red-200 ring-1 ring-red-500/20 flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2">
            <svg className="h-5 w-5 flex-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            {error}
          </div>
        ) : null
      }
    />
  )
}
