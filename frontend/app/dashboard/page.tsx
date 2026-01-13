"use client"

import { useEffect, useMemo, useRef, useState } from "react"

import { CandleCard } from "../../components/CandleCard"
import { Segmented } from "../../components/Segmented"

type StreamInit = {
  type: "init"
  mode: "realtime" | "playback"
  symbol: string
  bars: any[]
  cursor?: number
}
type StreamBar = { type: "bar"; mode: "realtime" | "playback"; symbol: string; bar: any; i?: number }
type StreamDone = { type: "done"; mode: "realtime" | "playback"; cursor?: number }
type StreamError = { type: "error"; message: string }
type StreamMessage = StreamInit | StreamBar | StreamDone | StreamError

const DEFAULT_SYMBOLS = ["META", "NVDA", "TSM", "PLTR", "AAPL", "NFLX"]

function toRFC3339FromPSTInput(v: string): string | null {
  if (!v) return null
  // v format is "YYYY-MM-DDTHH:mm"
  // Treat input string as PST (UTC-8) time
  // e.g. "2026-01-09T14:40" -> "2026-01-09T22:40:00Z"
  const [datePart, timePart] = v.split("T")
  if (!datePart || !timePart) return null
  
  const [year, month, day] = datePart.split("-").map(Number)
  const [hour, minute] = timePart.split(":").map(Number)
  
  // Construct UTC date from PST input: PST = UTC-8, so UTC = PST + 8h
  const d = new Date(Date.UTC(year, month - 1, day, hour + 8, minute))
  if (Number.isNaN(d.getTime())) return null
  return d.toISOString()
}

export default function DashboardPage() {
  const [mode, setMode] = useState<"realtime" | "playback">("playback")
  const [symbols, setSymbols] = useState(DEFAULT_SYMBOLS)
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackCursor, setPlaybackCursor] = useState(0)
  const [wsToken, setWsToken] = useState(0)
  const [startLocal, setStartLocal] = useState("2026-01-09T06:31")
  const [error, setError] = useState<string | null>(null)
  const [prevCloseBySymbol, setPrevCloseBySymbol] = useState<Record<string, number | null>>({})

  const [barsBySymbol, setBarsBySymbol] = useState<Record<string, any[]>>(() =>
    Object.fromEntries(symbols.map((s) => [s, []])),
  )

  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const reconnectTimerRef = useRef<number | null>(null)
  const playbackCursorRef = useRef(0)

  const symbolsParam = useMemo(() => symbols.join(","), [symbols])
  const startRFC = useMemo(() => toRFC3339FromPSTInput(startLocal), [startLocal])
  const shouldConnect = mode === "realtime" || (mode === "playback" && isPlaying)
  const asofRFC = useMemo(() => (mode === "playback" ? startRFC : new Date().toISOString()), [mode, startRFC])

  useEffect(() => {
    setBarsBySymbol((prev) => {
      const next: Record<string, any[]> = { ...prev }
      for (const s of symbols) next[s] ??= []
      for (const k of Object.keys(next)) if (!symbols.includes(k)) delete next[k]
      return next
    })
  }, [symbols])

  useEffect(() => {
    if (!asofRFC) return
    const base =
      process.env.NEXT_PUBLIC_BACKEND_HTTP ??
      `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_HTTP_PORT ?? "8001"}`

    const url = `${base}/api/stocks/prev_close?symbols=${encodeURIComponent(symbolsParam)}&asof=${encodeURIComponent(
      asofRFC,
    )}`

    let cancelled = false
    ;(async () => {
      try {
        const r = await fetch(url)
        if (!r.ok) return
        const payload = (await r.json()) as { prev_close?: Record<string, number | null> }
        if (cancelled) return
        setPrevCloseBySymbol(payload.prev_close ?? {})
      } catch {
        if (cancelled) return
        setPrevCloseBySymbol({})
      }
    })()

    return () => {
      cancelled = true
    }
  }, [asofRFC, symbolsParam])

  useEffect(() => {
    if (reconnectTimerRef.current) {
      window.clearTimeout(reconnectTimerRef.current)
      reconnectTimerRef.current = null
    }

    intentionalCloseRef.current = true
    wsRef.current?.close()
    wsRef.current = null

    if (!shouldConnect) return

    intentionalCloseRef.current = false
    setError(null)

    const base =
      process.env.NEXT_PUBLIC_BACKEND_WS ??
      `ws://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_WS_PORT ?? "8001"}`
    const url =
      mode === "realtime"
        ? `${base}/ws/realtime?symbols=${encodeURIComponent(symbolsParam)}`
        : `${base}/ws/playback?symbols=${encodeURIComponent(symbolsParam)}${
            startRFC ? `&start=${encodeURIComponent(startRFC)}` : ""
          }&speed=1&cursor=${encodeURIComponent(
            String(playbackCursorRef.current),
          )}`

    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onmessage = (ev) => {
      let msg: StreamMessage
      try {
        msg = JSON.parse(ev.data)
      } catch {
        return
      }
      if (msg.type === "error") {
        setError(msg.message)
        return
      }
      if (msg.type === "init") {
        if (typeof msg.cursor === "number") {
          playbackCursorRef.current = msg.cursor
          setPlaybackCursor(msg.cursor)
        }
        setBarsBySymbol((prev) => {
          const existing = prev[msg.symbol] ?? []
          if (existing.length > 0) return prev
          return { ...prev, [msg.symbol]: msg.bars }
        })
        
        // 检查实际返回数据的时间是否与用户选择的差异过大（>1天）
        if (mode === "playback" && msg.bars && msg.bars.length > 0) {
          const firstBar = msg.bars[msg.bars.length - 1]
          if (firstBar && firstBar.t) {
            const barTime = new Date(firstBar.t).getTime()
            const userTime = new Date(startLocal).getTime()
            if (Math.abs(barTime - userTime) > 24 * 60 * 60 * 1000) {
              setError(`所选时间无数据，已自动回退到最近交易日 (${new Date(firstBar.t).toLocaleDateString()})`)
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
        setBarsBySymbol((prev) => {
          const cur = prev[msg.symbol] ?? []
          const next = [...cur, msg.bar].slice(-800)
          return { ...prev, [msg.symbol]: next }
        })
        return
      }
      if (msg.type === "done") {
        if (typeof msg.cursor === "number") {
          playbackCursorRef.current = msg.cursor
          setPlaybackCursor(msg.cursor)
        }
        setIsPlaying(false)
        setError(null)
      }
    }

    ws.onerror = () => {
      if (intentionalCloseRef.current) return
      setError("WebSocket 连接失败（确认后端 WS 在跑）")
    }

    ws.onclose = (ev) => {
      if (intentionalCloseRef.current) return
      if (!shouldConnect) return
      if (ev.code === 1000) return

      reconnectTimerRef.current = window.setTimeout(() => {
        if (!intentionalCloseRef.current) {
          setError(`WebSocket 断开（${ev.code}），正在重连…`)
          setWsToken((t) => t + 1)
        }
      }, 600)
    }

    return () => {
      intentionalCloseRef.current = true
      ws.close()
    }
  }, [mode, symbolsParam, startRFC, shouldConnect, wsToken])

  useEffect(() => {
    if (mode === "realtime") setIsPlaying(true)
  }, [mode])

  return (
    <main className="min-h-screen bg-neon-radial">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="flex flex-col gap-6">
          <div className="rounded-3xl bg-white/6 p-5 shadow-glass ring-1 ring-white/10 backdrop-blur-xl">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div className="min-w-0">
                <div className="text-xs font-semibold text-white/60">0DTE Copilot</div>
                <div className="mt-1 text-2xl font-black tracking-tight">
                  Dashboard Grid <span className="text-white/60">({mode})</span>
                </div>
                <div className="mt-2 text-sm text-white/65">
                  回放模式会按分钟K线节奏推送更新，你可以像看直播一样复盘。
                </div>
                <div className="mt-2 flex flex-wrap items-center gap-2 text-xs font-semibold text-white/60">
                  <span className="rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">Timeframe: 1 Minute</span>
                  <div className="flex items-center gap-1.5 rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">
                    <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                    <span>EMA 9</span>
                  </div>
                  <div className="flex items-center gap-1.5 rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">
                    <div className="h-1.5 w-1.5 rounded-full bg-red-400 shadow-[0_0_8px_rgba(248,113,113,0.5)]" />
                    <span>EMA 21</span>
                  </div>
                  <div className="flex items-center gap-1.5 rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">
                    <div className="h-1.5 w-1.5 rounded-full bg-slate-50 shadow-[0_0_8px_rgba(248,250,252,0.5)]" />
                    <span>VWAP</span>
                  </div>
                  <div className="flex items-center gap-1.5 rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">
                    <div className="h-1.5 w-1.5 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.5)]" />
                    <span>BB Upper</span>
                  </div>
                  <div className="flex items-center gap-1.5 rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">
                    <div className="h-1.5 w-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]" />
                    <span>BB Middle</span>
                  </div>
                  <div className="flex items-center gap-1.5 rounded-full bg-white/5 px-3 py-1 ring-1 ring-white/10">
                    <div className="h-1.5 w-1.5 rounded-full bg-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.5)]" />
                    <span>BB Lower</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <Segmented<"realtime" | "playback">
                  value={mode}
                  onChange={setMode}
                  segments={[
                    { value: "playback", label: "Playback" },
                    { value: "realtime", label: "Realtime" },
                  ]}
                  className="w-full sm:w-[240px]"
                />

                {mode === "playback" ? (
                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      onClick={() => {
                        if (isPlaying) {
                          intentionalCloseRef.current = true
                          wsRef.current?.close()
                          wsRef.current = null
                          setIsPlaying(false)
                          return
                        }
                        intentionalCloseRef.current = false
                        setError(null)
                        setIsPlaying(true)
                        setWsToken((t) => t + 1)
                      }}
                      className="rounded-2xl bg-white/10 px-4 py-2 text-xs font-semibold text-white/85 ring-1 ring-white/10 backdrop-blur-md hover:bg-white/12"
                    >
                      {isPlaying ? "Pause" : "Start"}
                    </button>
                    <div className="flex items-center gap-2 rounded-2xl bg-black/30 px-3 py-2 text-xs text-white/80 ring-1 ring-white/10">
                      <span className="font-semibold text-white/60">PST</span>
                      <input
                        value={startLocal}
                        onChange={(e) => {
                          setBarsBySymbol(Object.fromEntries(symbols.map((s) => [s, []])))
                          playbackCursorRef.current = 0
                          setPlaybackCursor(0)
                          setStartLocal(e.target.value)
                          setIsPlaying(false)
                          setWsToken((t) => t + 1)
                        }}
                        type="datetime-local"
                        className="bg-transparent outline-none"
                      />
                    </div>
                  </div>
                ) : null}
              </div>
            </div>

            {error ? (
              <div className="mt-4 rounded-2xl bg-red-500/10 px-4 py-3 text-sm text-red-200 ring-1 ring-red-500/20">
                {error}
              </div>
            ) : null}
          </div>

          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
            {symbols.map((sym) => (
              <CandleCard
                key={sym}
                symbol={sym}
                bars={barsBySymbol[sym] ?? []}
                percentChange={
                  (() => {
                    const bars = barsBySymbol[sym] ?? []
                    const last = bars.length ? bars[bars.length - 1] : null
                    const lastClose = typeof last?.c === "number" ? last.c : null
                    const prev = prevCloseBySymbol[sym]
                    if (!lastClose || !prev) return null
                    return ((lastClose - prev) / prev) * 100
                  })()
                }
                status="normal"
              />
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}
