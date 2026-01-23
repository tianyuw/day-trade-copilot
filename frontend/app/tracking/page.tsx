"use client"

import Link from "next/link"
import { useEffect, useMemo, useRef, useState } from "react"
import { motion } from "framer-motion"
import { TrackingMiniChart } from "../../components/TrackingMiniChart"
import { cn } from "../../components/cn"

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
type StreamState = {
  type: "state"
  mode: "realtime" | "playback"
  symbol: string
  state: string
  in_position: boolean
  contracts_total?: number | null
  contracts_remaining?: number | null
  trade_id?: string | null
  option?: { right: "call" | "put"; expiration: string; strike: number } | null
  option_symbol?: string | null
}
type StreamPosition = { type: "position"; mode: "realtime" | "playback"; symbol: string; result: any }
type StreamMessage = StreamInit | StreamBar | StreamAnalysis | StreamState | StreamPosition | StreamDone | StreamError

type MarketStatus = {
  server_time: string
  session: "pre_market" | "regular" | "after_hours" | "closed"
  is_open: boolean
  next_open: string
  next_close: string
}

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

type SymbolSuggestion = { symbol: string; name?: string; exchange?: string }

const DEFAULT_WATCHLIST = ["META", "NVDA", "TSM", "PLTR", "AAPL", "NFLX", "SPY", "QQQ"]
const WATCHLIST_STORAGE_KEY = "tracking:watchlist"

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
  if (session === "regular") return "bg-emerald-500/10 text-emerald-300 ring-1 ring-emerald-500/30"
  if (session === "pre_market") return "bg-cyan-500/10 text-cyan-200 ring-1 ring-cyan-500/30"
  if (session === "after_hours") return "bg-violet-500/10 text-violet-200 ring-1 ring-violet-500/30"
  return "bg-white/5 text-white/50 ring-1 ring-white/10"
}

function saveAnalysis(result: AnalysisResult) {
  try {
    localStorage.setItem(`analysis:${result.analysis_id}`, JSON.stringify(result))
  } catch {}
}

export default function TrackingPage() {
  const [watchlist, setWatchlist] = useState<string[]>(DEFAULT_WATCHLIST.slice(0, 10))
  const [watchlistHydrated, setWatchlistHydrated] = useState(false)
  const [input, setInput] = useState("")
  const [isAddOpen, setIsAddOpen] = useState(false)
  const [suggestions, setSuggestions] = useState<SymbolSuggestion[]>([])
  const [isEditing, setIsEditing] = useState(false)
  const [barsBySymbol, setBarsBySymbol] = useState<Record<string, any[]>>({})
  const [analysisBySymbol, setAnalysisBySymbol] = useState<Record<string, AnalysisResult | null>>({})
  const [sessionBySymbol, setSessionBySymbol] = useState<
    Record<
      string,
      {
        state: string
        inPosition: boolean
        contractsRemaining: number | null
        contractsTotal: number | null
      }
    >
  >({})
  const [prevCloseBySymbol, setPrevCloseBySymbol] = useState<Record<string, number | null>>({})
  const [market, setMarket] = useState<MarketStatus | null>(null)
  const [wsStatus, setWsStatus] = useState<"connecting" | "open" | "closed" | "error">("closed")
  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const addInputRef = useRef<HTMLInputElement | null>(null)
  const pressTimerRef = useRef<number | null>(null)
  const suppressNextClickRef = useRef(false)

  const symbolsParam = useMemo(() => watchlist.join(","), [watchlist])

  useEffect(() => {
    try {
      const raw = localStorage.getItem(WATCHLIST_STORAGE_KEY)
      if (raw) {
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) {
          const cleaned = parsed
            .map((x) => String(x ?? "").trim().toUpperCase())
            .filter(Boolean)
          const uniq = Array.from(new Set(cleaned))
          if (uniq.length) setWatchlist(uniq.slice(0, 10))
        }
      }
    } catch {}
    setWatchlistHydrated(true)
  }, [])

  useEffect(() => {
    if (!watchlistHydrated) return
    try {
      localStorage.setItem(WATCHLIST_STORAGE_KEY, JSON.stringify(watchlist))
    } catch {}
  }, [watchlist, watchlistHydrated])

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key !== "Escape") return
      setIsAddOpen(false)
      setIsEditing(false)
    }
    window.addEventListener("keydown", onKeyDown)
    return () => window.removeEventListener("keydown", onKeyDown)
  }, [])

  useEffect(() => {
    if (!isAddOpen) return
    const t = window.setTimeout(() => addInputRef.current?.focus(), 0)
    return () => window.clearTimeout(t)
  }, [isAddOpen])

  useEffect(() => {
    if (!isAddOpen) return
    const q = input.trim()
    if (!q) {
      setSuggestions([])
      return
    }

    const controller = new AbortController()
    const t = window.setTimeout(async () => {
      try {
        const base =
          process.env.NEXT_PUBLIC_BACKEND_API ??
          `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
        const res = await fetch(`${base}/api/stocks/symbols?query=${encodeURIComponent(q)}&limit=20`, { signal: controller.signal })
        if (!res.ok) throw new Error("symbols failed")
        const data = await res.json()
        const raw = Array.isArray(data?.symbols) ? (data.symbols as SymbolSuggestion[]) : []
        const existing = new Set(watchlist)
        setSuggestions(raw.filter((x) => x?.symbol && !existing.has(String(x.symbol).toUpperCase())))
      } catch {
        if (!controller.signal.aborted) setSuggestions([])
      }
    }, 200)

    return () => {
      window.clearTimeout(t)
      controller.abort()
    }
  }, [input, isAddOpen, watchlist])

  useEffect(() => {
    async function fetchMarket() {
      try {
        const base =
          process.env.NEXT_PUBLIC_BACKEND_API ??
          `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
        const res = await fetch(`${base}/api/market/status`)
        if (!res.ok) throw new Error("market status failed")
        const data = (await res.json()) as MarketStatus
        setMarket(data)
      } catch {
        setMarket(null)
      }
    }
    fetchMarket()
    const t = setInterval(fetchMarket, 30_000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    async function fetchPrevClose() {
      try {
        const base =
          process.env.NEXT_PUBLIC_BACKEND_API ??
          `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
        const asof = new Date().toISOString()
        const res = await fetch(`${base}/api/stocks/prev_close?symbols=${encodeURIComponent(symbolsParam)}&asof=${encodeURIComponent(asof)}`)
        if (!res.ok) throw new Error("prev_close failed")
        const data = await res.json()
        setPrevCloseBySymbol((data?.prev_close ?? {}) as Record<string, number | null>)
      } catch {
        setPrevCloseBySymbol({})
      }
    }
    if (watchlist.length > 0) fetchPrevClose()
  }, [symbolsParam, watchlist.length])

  useEffect(() => {
    intentionalCloseRef.current = true
    wsRef.current?.close()
    wsRef.current = null

    if (watchlist.length === 0) return

    intentionalCloseRef.current = false
    setWsStatus("connecting")

    const base =
      process.env.NEXT_PUBLIC_BACKEND_WS ??
      `ws://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_WS_PORT ?? "8000"}`
    const url = `${base}/ws/realtime?symbols=${encodeURIComponent(symbolsParam)}&analyze=true`

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
        return
      }

      if (msg.type === "init") {
        setBarsBySymbol((prev) => ({ ...prev, [msg.symbol]: msg.bars || [] }))
      } else if (msg.type === "bar") {
        setBarsBySymbol((prev) => ({
          ...prev,
          [msg.symbol]: [...(prev[msg.symbol] ?? []), msg.bar].slice(-500),
        }))
      } else if (msg.type === "analysis") {
        const res = msg.result as AnalysisResult
        setAnalysisBySymbol((prev) => ({ ...prev, [msg.symbol]: res }))
        if (res?.analysis_id) saveAnalysis(res)
      } else if (msg.type === "state") {
        setSessionBySymbol((prev) => ({
          ...prev,
          [msg.symbol]: {
            state: msg.state,
            inPosition: msg.in_position,
            contractsRemaining: msg.contracts_remaining ?? null,
            contractsTotal: msg.contracts_total ?? null,
          },
        }))
      }
    }

    return () => {
      intentionalCloseRef.current = true
      ws.close()
    }
  }, [symbolsParam, watchlist.length])

  const sortedSymbols = useMemo(() => {
    const inPos: string[] = []
    const rest: string[] = []
    for (const sym of watchlist) {
      const sess = sessionBySymbol[sym]
      if (sess?.inPosition && (sess.contractsRemaining ?? 0) > 0) inPos.push(sym)
      else rest.push(sym)
    }
    return [...inPos, ...rest]
  }, [sessionBySymbol, watchlist])

  const countdown = useMemo(() => {
    if (!market) return null
    const now = Date.now()
    const target = market.session === "regular" ? Date.parse(market.next_close) : Date.parse(market.next_open)
    if (!Number.isFinite(target)) return null
    return { label: market.session === "regular" ? "Until Close" : "Until Open", ms: target - now }
  }, [market])

  const addSymbol = (raw: string) => {
    const s = raw.trim().toUpperCase()
    if (!s) return
    if (watchlist.length >= 10) return
    if (watchlist.includes(s)) {
      setInput("")
      return
    }
    setInput("")
    setWatchlist((prev) => {
      if (prev.includes(s)) return prev
      const next = [s, ...prev]
      return next.slice(0, 10)
    })
    setSuggestions([])
    setIsAddOpen(false)
  }

  const removeSymbol = (sym: string) => {
    setWatchlist((prev) => prev.filter((x) => x !== sym))
    setBarsBySymbol((prev) => {
      const next = { ...prev }
      delete next[sym]
      return next
    })
    setAnalysisBySymbol((prev) => {
      const next = { ...prev }
      delete next[sym]
      return next
    })
    setIsEditing(false)
  }

  return (
    <main className="flex min-h-screen flex-col bg-neon-radial text-white font-sans">
      <div className="flex-none border-b border-white/10 bg-black/20 backdrop-blur-xl px-6 py-4">
        <div className="mx-auto flex max-w-[1600px] flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="text-xs font-medium text-white/40 uppercase tracking-wider">Market</div>
              <div className={cn("flex items-center gap-2 rounded-full px-3 py-1 text-xs font-bold", marketPillClass(market?.session ?? "closed"))}>
                <span className={cn("h-2 w-2 rounded-full", market?.session === "regular" ? "bg-emerald-400" : market?.session === "closed" ? "bg-white/30" : "bg-cyan-400")} />
                {market ? marketLabel(market.session) : "Unknown"}
              </div>
              {countdown && (
                <div className="hidden sm:flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-xs font-mono text-white/60 ring-1 ring-white/10">
                  <span className="text-white/40">{countdown.label}</span>
                  <span>{formatCountdown(countdown.ms)}</span>
                </div>
              )}
            </div>

            <div className="h-8 w-px bg-white/10 hidden lg:block" />

            <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-xs font-bold text-white/60 ring-1 ring-white/10">
              <span
                className={cn(
                  "h-2 w-2 rounded-full",
                  wsStatus === "open" ? "bg-emerald-400" : wsStatus === "connecting" ? "bg-cyan-400" : wsStatus === "error" ? "bg-red-400" : "bg-white/30",
                )}
              />
              {wsStatus === "open" ? "AI Monitoring" : wsStatus === "connecting" ? "Connecting" : wsStatus === "error" ? "Error" : "Disconnected"}
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 p-6">
        <div className="mx-auto max-w-[1600px]">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {sortedSymbols.map((sym) => {
              const bars = barsBySymbol[sym] ?? []
              const last = bars.length ? bars[bars.length - 1] : null
              const prevClose = prevCloseBySymbol[sym]
              const price = typeof last?.c === "number" ? last.c : null
              const changePct =
                typeof price === "number" && typeof prevClose === "number" && prevClose !== 0
                  ? ((price - prevClose) / prevClose) * 100
                  : null
              const a = analysisBySymbol[sym]
              const sess = sessionBySymbol[sym]
              const inPosition = sess?.inPosition && (sess.contractsRemaining ?? 0) > 0
              const hasSignal = a && (a.action === "buy_long" || a.action === "buy_short")
              const border =
                inPosition && sess?.state === "IN_POSITION"
                  ? "border-emerald-400/70 ring-2 ring-emerald-400/70 shadow-[0_0_24px_rgba(34,197,94,0.55)]"
                  : hasSignal && a?.action === "buy_long"
                    ? "border-emerald-500/50 ring-2 ring-emerald-500/55 shadow-[0_0_18px_rgba(34,197,94,0.35)]"
                    : hasSignal && a?.action === "buy_short"
                      ? "border-red-500/50 ring-2 ring-red-500/55 shadow-[0_0_18px_rgba(239,68,68,0.35)]"
                      : ""

              const href = a?.analysis_id ? `/tracking/${sym}?analysis_id=${encodeURIComponent(a.analysis_id)}` : `/tracking/${sym}`

              return (
                <motion.div layout key={sym}>
                <Link
                  key={sym}
                  href={href}
                  onPointerDown={(e) => {
                    if (isEditing) return
                    if (e.pointerType === "mouse" && e.button !== 0) return
                    if (pressTimerRef.current != null) window.clearTimeout(pressTimerRef.current)
                    pressTimerRef.current = window.setTimeout(() => {
                      setIsEditing(true)
                      suppressNextClickRef.current = true
                      if (typeof navigator !== "undefined" && "vibrate" in navigator) (navigator as any).vibrate?.(12)
                    }, 450)
                  }}
                  onPointerUp={() => {
                    if (pressTimerRef.current != null) window.clearTimeout(pressTimerRef.current)
                    pressTimerRef.current = null
                  }}
                  onPointerCancel={() => {
                    if (pressTimerRef.current != null) window.clearTimeout(pressTimerRef.current)
                    pressTimerRef.current = null
                  }}
                  onPointerLeave={() => {
                    if (pressTimerRef.current != null) window.clearTimeout(pressTimerRef.current)
                    pressTimerRef.current = null
                  }}
                  onClick={(e) => {
                    if (isEditing || suppressNextClickRef.current) {
                      e.preventDefault()
                      e.stopPropagation()
                      suppressNextClickRef.current = false
                    }
                  }}
                  className={cn(
                    "block h-full group relative overflow-hidden rounded-2xl border border-white/10 p-4 transition hover:border-white/20 hover:bg-black/45 bg-black/40",
                    inPosition ? "animate-[bgPulse_2.4s_ease_infinite]" : "",
                    border,
                  )}
                >
                  {isEditing && (
                    <button
                      type="button"
                      aria-label={`Remove ${sym}`}
                      onClick={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        removeSymbol(sym)
                      }}
                      className="absolute right-3 top-3 z-20 inline-flex h-8 w-8 items-center justify-center rounded-full bg-black/70 text-white/80 ring-1 ring-white/15 hover:bg-black/80"
                    >
                      ×
                    </button>
                  )}
                  <div className="relative">
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <div className="flex items-baseline gap-2">
                          <div className="text-xl font-black tracking-tight">{sym}</div>
                          {typeof price === "number" && (
                            <div className="text-sm font-mono text-white/80">{price.toFixed(2)}</div>
                          )}
                          {typeof changePct === "number" && (
                            <div className={cn("text-xs font-bold", changePct >= 0 ? "text-emerald-400" : "text-red-400")}>
                              {changePct >= 0 ? "+" : ""}
                              {changePct.toFixed(2)}%
                            </div>
                          )}
                        </div>
                        <div className="mt-1 flex items-center gap-2 text-xs text-white/50">
                          <div className="truncate">
                            {a?.pattern_name ? a.pattern_name : a?.action ? a.action.replace(/_/g, " ") : "Scanning"}
                          </div>
                          {a?.confidence != null && (
                            <div className="flex-none font-mono text-white/40">{Math.round(a.confidence * 100)}%</div>
                          )}
                        </div>
                      </div>

                      <div
                        className={cn(
                          "flex-none rounded-lg px-2 py-1 text-[10px] font-black uppercase tracking-wider",
                          hasSignal
                            ? a?.action === "buy_long"
                              ? "bg-emerald-500/20 text-emerald-200 ring-1 ring-emerald-500/40"
                              : "bg-red-500/20 text-red-200 ring-1 ring-red-500/40"
                            : "bg-white/5 text-white/50 ring-1 ring-white/10",
                        )}
                      >
                        {hasSignal ? (a!.action === "buy_long" ? "BUY LONG" : "BUY SHORT") : "SCANNING"}
                      </div>
                    </div>

                    <div className="mt-3">
                      <TrackingMiniChart bars={bars} />
                    </div>
                  </div>
                </Link>
                </motion.div>
              )
            })}

            <button
              type="button"
              onClick={() => {
                if (watchlist.length >= 10) return
                setIsEditing(false)
                setInput("")
                setSuggestions([])
                setIsAddOpen(true)
              }}
              disabled={watchlist.length >= 10}
              className={cn(
                "relative flex min-h-[168px] items-center justify-center rounded-2xl border border-dashed bg-black/20 backdrop-blur-md transition",
                watchlist.length >= 10
                  ? "cursor-not-allowed border-white/10 text-white/25"
                  : "border-white/25 text-white/60 hover:border-white/40 hover:bg-black/30",
              )}
            >
              <div className="text-center">
                <div className="text-3xl font-black leading-none">+</div>
                <div className="mt-2 text-xs font-mono">{watchlist.length >= 10 ? "Max 10" : "Add Ticker"}</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      {isAddOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) setIsAddOpen(false)
          }}
        >
          <div className="w-full max-w-xl rounded-2xl bg-black/70 backdrop-blur-xl ring-1 ring-white/15">
            <div className="flex items-center justify-between gap-3 border-b border-white/10 px-5 py-4">
              <div className="text-sm font-bold text-white/80">Add Ticker</div>
              <button
                type="button"
                onClick={() => setIsAddOpen(false)}
                className="rounded-lg bg-white/5 px-3 py-1.5 text-xs font-bold text-white/70 ring-1 ring-white/10 hover:bg-white/10"
              >
                Close
              </button>
            </div>

            <div className="p-5">
              <div className="flex items-center gap-2 rounded-xl bg-black/40 px-4 py-3 ring-1 ring-white/10">
                <input
                  ref={addInputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") addSymbol(input)
                  }}
                  placeholder="Search ticker (e.g. TSLA)"
                  className="w-full bg-transparent text-sm font-mono text-white outline-none placeholder:text-white/30"
                />
                <button
                  type="button"
                  onClick={() => addSymbol(input)}
                  className="rounded-lg bg-white text-black px-3 py-1.5 text-xs font-bold hover:bg-cyan-50"
                >
                  Add
                </button>
              </div>

              {suggestions.length > 0 && (
                <div className="mt-4 max-h-72 overflow-auto rounded-xl bg-black/30 ring-1 ring-white/10">
                  {suggestions.map((sug) => (
                    <button
                      key={sug.symbol}
                      type="button"
                      onClick={() => addSymbol(sug.symbol)}
                      className="flex w-full items-center justify-between gap-4 px-4 py-3 text-left text-sm text-white/75 hover:bg-white/5"
                    >
                      <div className="min-w-0">
                        <div className="font-mono font-bold text-white/85">{String(sug.symbol).toUpperCase()}</div>
                        {sug.name && <div className="truncate text-xs text-white/40">{sug.name}</div>}
                      </div>
                      {sug.exchange && <div className="flex-none text-[10px] font-bold text-white/35">{String(sug.exchange)}</div>}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
