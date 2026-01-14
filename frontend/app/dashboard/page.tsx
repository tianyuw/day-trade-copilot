"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import { CandleCard } from "../../components/CandleCard"

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

type ChatMessage = { role: "ai" | "system"; content: string; time: string }

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

function AICopilotPanel({ symbol, lastBar, resetToken }: { symbol: string; lastBar: any; resetToken: number }) {
  const [messages, setMessages] = useState<ChatMessage[]>([])

  useEffect(() => {
    // Force reset state
    setMessages([
      {
        role: "system",
        content: `AI Copilot initialized for ${symbol}. Monitoring price action...`,
        time: new Date().toLocaleTimeString(),
      },
    ])
  }, [symbol, resetToken])

  useEffect(() => {
    if (!lastBar) return
    const random = Math.random()
    if (random > 0.9) {
      const price = lastBar.c
      const isUp = lastBar.c > lastBar.o
      const msg = isUp
        ? `Bullish momentum detected on ${symbol} at ${price.toFixed(2)}. Volume spike supports continuation.`
        : `Selling pressure increasing on ${symbol} near ${price.toFixed(2)}. Watch for support breakdown.`

      setMessages((prev) => {
        const next: ChatMessage[] = [
          ...prev,
          { role: "ai", content: msg, time: new Date().toLocaleTimeString() },
        ]
        return next.slice(-5)
      })
    }
  }, [lastBar, symbol])

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-3xl bg-white/5 shadow-glass ring-1 ring-white/10 backdrop-blur-xl">
      <div className="border-b border-white/10 bg-white/5 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="grid h-8 w-8 place-items-center rounded-lg bg-indigo-500/20 ring-1 ring-indigo-500/50">
             <svg className="h-4 w-4 text-indigo-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
             </svg>
          </div>
          <div>
            <h3 className="font-bold text-white">AI Copilot</h3>
            <p className="text-xs text-white/50">Gemini 3 Pro • Realtime Analysis</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-4 ${msg.role === "system" ? "opacity-50" : ""}`}>
            <div
              className={`mt-1 h-2 w-2 flex-none rounded-full ${
                msg.role === "system"
                  ? "bg-white/30"
                  : "bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.5)]"
              }`}
            />
            <div className="space-y-1">
              <div className="text-xs font-mono text-white/30">{msg.time}</div>
              <p className="text-sm leading-relaxed text-white/90">{msg.content}</p>
            </div>
          </div>
        ))}
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-sm text-white/30">Waiting for market data...</div>
        )}
      </div>

      <div className="border-t border-white/10 bg-black/20 px-6 py-4">
        <div className="flex items-center gap-2 rounded-xl bg-white/5 px-4 py-2 ring-1 ring-white/10">
          <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs font-medium text-white/50">Live Connection Active</span>
        </div>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const [selectedSymbol, setSelectedSymbol] = useState("NVDA")
  const [startLocal, setStartLocal] = useState("2026-01-09T06:31")
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackCursor, setPlaybackCursor] = useState(0)
  const [wsToken, setWsToken] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [resetToken, setResetToken] = useState(0)
  const [prevClose, setPrevClose] = useState<number | null>(null)

  const [bars, setBars] = useState<any[]>([])

  const wsRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const playbackCursorRef = useRef(0)

  const startRFC = useMemo(() => toRFC3339FromPSTInput(startLocal), [startLocal])

  useEffect(() => {
    async function fetchPrevClose() {
      try {
        const base =
          process.env.NEXT_PUBLIC_BACKEND_API ??
          `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8001"}`
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
      `ws://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_WS_PORT ?? "8001"}`
    const url = `${base}/ws/playback?symbols=${encodeURIComponent(selectedSymbol)}&start=${encodeURIComponent(
      startRFC ?? "",
    )}&speed=1&cursor=${encodeURIComponent(String(playbackCursorRef.current))}`

    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onmessage = (ev) => {
      let msg: StreamMessage
      try {
        msg = JSON.parse(ev.data)
      } catch { return }

      if (msg.type === "error") {
        setError(msg.message)
        setIsPlaying(false)
        return
      }

      if (msg.type === "init") {
        if (typeof msg.cursor === "number") {
          playbackCursorRef.current = msg.cursor
          setPlaybackCursor(msg.cursor)
        }
        if (msg.symbol === selectedSymbol) {
          setBars(msg.bars || [])
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
      } else if (msg.type === "bar") {
        if (typeof msg.i === "number") {
          playbackCursorRef.current = msg.i + 1
          setPlaybackCursor(msg.i + 1)
        }
        if (msg.symbol === selectedSymbol) {
          setBars((prev) => [...prev, msg.bar].slice(-1000))
        }
      } else if (msg.type === "done") {
        setIsPlaying(false)
      }
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
                  {DEFAULT_SYMBOLS.map(s => <option key={s} value={s} className="bg-slate-900">{s}</option>)}
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
                  onClick={() => setIsPlaying(!isPlaying)}
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
            <AICopilotPanel symbol={selectedSymbol} lastBar={bars[bars.length - 1]} resetToken={resetToken} />
          </div>

        </div>
      </div>
    </main>
  )
}
