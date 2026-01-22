"use client"

import { useEffect, useRef } from "react"
import { cn } from "./cn"

type AnalysisResult = {
  action: "buy_long" | "buy_short" | "ignore" | "follow_up" | "check_when_condition_meet"
  confidence: number
  reasoning: string
  pattern_name?: string
  breakout_price?: number
  watch_condition?: {
    trigger_price: number
    direction: "above" | "below"
    expiry_minutes: number
  }
  trade_plan?: {
    trade_id: string
    direction: "long" | "short"
    option: { right: "call" | "put"; expiration: string; strike: number }
    contracts: number
    risk?: { stop_loss_premium: number; time_stop_minutes: number }
    take_profit_premium?: number
  } | null
  entry?: { option_symbol?: string | null } | null
}

export type ChatMessage = {
  role: "ai" | "system"
  content: string | AnalysisResult
  time: string
  type?: "analysis" | "text"
}

export function AICopilot({ 
  symbol, 
  messages 
}: { 
  symbol: string
  messages: ChatMessage[]
}) {
  const bottomRef = useRef<HTMLDivElement>(null)

  const renderPositionMgmtCard = (raw: string) => {
    const lines = raw.split("\n")
    const header = String(lines[0] ?? "")
    const decision = header.includes(":") ? header.split(":").slice(1).join(":").trim() : header.trim()
    const reasoning = String(lines[1] ?? "").trim()
    const meta = lines
      .slice(2)
      .map((l) => String(l ?? "").trim())
      .filter(Boolean)

    const parsed = meta
      .map((m) => {
        const idx = m.indexOf("=")
        if (idx <= 0) return null
        return { key: m.slice(0, idx).trim(), value: m.slice(idx + 1).trim(), raw: m }
      })
      .filter((x): x is { key: string; value: string; raw: string } => Boolean(x))

    const kv: Record<string, string> = {}
    for (const p of parsed) kv[p.key] = p.value

    const knownKeys = new Set([
      "last_px",
      "contracts",
      "direction",
      "option",
      "option_symbol",
      "stop_loss_premium",
      "take_profit_premium",
      "time_stop_minutes",
    ])
    const extraMeta = meta.filter((m) => {
      const idx = m.indexOf("=")
      if (idx <= 0) return true
      const k = m.slice(0, idx).trim()
      return !knownKeys.has(k)
    })

    const lastPx = kv.last_px
    const contracts = kv.contracts
    const direction = kv.direction ? kv.direction.toUpperCase() : ""
    const option = kv.option
    const optionSymbol = kv.option_symbol
    const sl = kv.stop_loss_premium
    const tp = kv.take_profit_premium
    const tstop = kv.time_stop_minutes
    const riskLineParts = [
      sl ? `SL ${sl}` : null,
      tp ? `TP ${tp}` : null,
      tstop ? `T ${tstop}m` : null,
    ].filter(Boolean) as string[]
    const riskLine = riskLineParts.length ? riskLineParts.join(" · ") : ""

    const decisionClass = cn(
      "px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider ring-1",
      decision === "close_all"
        ? "bg-red-500/20 text-red-200 ring-red-500/40"
        : decision === "close_partial"
          ? "bg-amber-500/20 text-amber-200 ring-amber-500/40"
          : decision === "hold"
            ? "bg-cyan-500/20 text-cyan-200 ring-cyan-500/40"
            : "bg-violet-500/20 text-violet-200 ring-violet-500/40",
    )

    return (
      <div className="mt-2 rounded-xl bg-white/5 p-4 ring-1 ring-white/10">
        <div className="flex items-center justify-between mb-3 gap-3">
          <div className="flex items-center gap-2 min-w-0">
            <div className={decisionClass}>{decision.replace(/_/g, " ")}</div>
            <div className="px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-200 ring-1 ring-indigo-500/30">
              position mgmt
            </div>
          </div>
          <div className="text-xs font-mono text-white/40" />
        </div>

        <div className="mb-3 flex flex-wrap gap-2">
          <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
            <span className="mr-1 opacity-50">Last Px:</span>
            {lastPx || "N/A"}
          </div>
          <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
            <span className="mr-1 opacity-50">Contracts:</span>
            {contracts || "N/A"}
          </div>
          <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
            <span className="mr-1 opacity-50">Dir:</span>
            {direction || "N/A"}
          </div>
          <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
            <span className="mr-1 opacity-50">Option:</span>
            {option || "N/A"}
          </div>
          <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
            <span className="mr-1 opacity-50">Symbol:</span>
            {optionSymbol || "N/A"}
          </div>
          <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
            <span className="mr-1 opacity-50">Risk:</span>
            {riskLine || "N/A"}
          </div>
        </div>

        {reasoning ? (
          <p className="text-sm text-white/80 leading-relaxed">{reasoning}</p>
        ) : (
          <p className="text-sm text-white/60 leading-relaxed">No reasoning provided.</p>
        )}

        {extraMeta.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2 border-t border-white/10 pt-3">
            {extraMeta.map((m, i) => (
              <div
                key={`${m}-${i}`}
                className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-mono text-white/70 ring-1 ring-white/10"
              >
                {m}
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

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
            <p className="text-xs text-white/50">Realtime Analysis · {symbol}</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
        {messages.map((msg, idx) => {
          if (
            msg.role === "system" &&
            typeof msg.content === "string" &&
            msg.content.startsWith("PLAN_READY → IN_POSITION")
          ) {
            return null
          }

          return (
            <div key={idx} className={`flex gap-4 ${msg.role === "system" ? "opacity-50" : ""}`}>
            <div
              className={`mt-1 h-2 w-2 flex-none rounded-full ${
                msg.role === "system"
                  ? "bg-white/30"
                  : "bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.5)]"
              }`}
            />
            <div className="space-y-1 w-full min-w-0">
              <div className="text-xs font-mono text-white/30">{msg.time}</div>
              
              {msg.type === "analysis" && typeof msg.content === "object" ? (
                <div className="mt-2 rounded-xl bg-white/5 p-4 ring-1 ring-white/10">
                    <div className="flex items-center justify-between mb-3">
                        <div className={cn(
                            "px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider",
                            msg.content.action === 'buy_long' ? "bg-emerald-500/20 text-emerald-300 ring-1 ring-emerald-500/50" :
                            msg.content.action === 'buy_short' ? "bg-red-500/20 text-red-300 ring-1 ring-red-500/50" :
                            "bg-white/10 text-white/60"
                        )}>
                            {msg.content.action.replace(/_/g, " ")}
                        </div>
                        <div className="text-xs font-mono text-white/40">
                            Conf: {(msg.content.confidence * 100).toFixed(0)}%
                        </div>
                    </div>
                    
                    {/* Pattern & Breakout Info */}
                    {(msg.content.pattern_name || msg.content.breakout_price) && (
                        <div className="mb-3 flex flex-wrap gap-2">
                            {msg.content.pattern_name && (
                                <div className="inline-flex items-center rounded-md bg-indigo-500/20 px-2 py-1 text-[10px] font-medium text-indigo-200 ring-1 ring-indigo-500/30">
                                    <svg className="mr-1 h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                    </svg>
                                    {msg.content.pattern_name}
                                </div>
                            )}
                            {msg.content.breakout_price && (
                                <div className="inline-flex items-center rounded-md bg-amber-500/20 px-2 py-1 text-[10px] font-medium text-amber-200 ring-1 ring-amber-500/30">
                                    <span className="mr-1 opacity-50">Breakout:</span>
                                    {msg.content.breakout_price}
                                </div>
                            )}
                        </div>
                    )}

                    <p className="text-sm text-white/80 leading-relaxed">
                        {msg.content.reasoning}
                    </p>
                    {msg.content.action === "follow_up" && (
                        <div className="mt-3 pt-3 border-t border-white/10 text-xs font-mono">
                            <span className="text-white/40">Follow-up: </span>
                            <span className="text-amber-300">re-verify on next 1m close</span>
                        </div>
                    )}
                    {msg.content.watch_condition && (
                        <div className="mt-3 pt-3 border-t border-white/10 text-xs font-mono">
                            <span className="text-white/40">Watch: </span>
                            <span className="text-amber-300">
                                {msg.content.watch_condition.direction} {msg.content.watch_condition.trigger_price}
                            </span>
                            <span className="text-white/30 ml-2">
                                (Expires in {msg.content.watch_condition.expiry_minutes}m)
                            </span>
                        </div>
                    )}
                    {(msg.content.action === "buy_long" || msg.content.action === "buy_short") && msg.content.trade_plan && (
                        <div className="mt-3 pt-3 border-t border-white/10">
                            <div className="flex items-center justify-between gap-3">
                                <div className="text-xs font-bold uppercase tracking-wider text-white/60">
                                    Entry
                                </div>
                                <div className="text-xs font-mono text-white/35" />
                            </div>

                            <div className="mt-2 flex flex-wrap gap-2">
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">trade_id:</span>
                                    {msg.content.trade_plan.trade_id}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">dir:</span>
                                    {msg.content.trade_plan.direction.toUpperCase()}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">contracts:</span>
                                    {msg.content.trade_plan.contracts}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">option:</span>
                                    {msg.content.trade_plan.option.right} {msg.content.trade_plan.option.expiration} {msg.content.trade_plan.option.strike}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">sl:</span>
                                    {msg.content.trade_plan.risk?.stop_loss_premium ?? "N/A"}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">tp:</span>
                                    {msg.content.trade_plan.take_profit_premium ?? "N/A"}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">t:</span>
                                    {(msg.content.trade_plan.risk?.time_stop_minutes ?? "N/A")}{msg.content.trade_plan.risk?.time_stop_minutes != null ? "m" : ""}
                                </div>
                                <div className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10">
                                    <span className="mr-1 opacity-50">option_symbol:</span>
                                    {msg.content.entry?.option_symbol ?? "N/A"}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
              ) : msg.role === "ai" && typeof msg.content === "string" && msg.content.startsWith("POSITION_MGMT:") ? (
                renderPositionMgmtCard(msg.content)
              ) : (
                <p className="text-sm leading-relaxed text-white/90 whitespace-pre-wrap">{msg.content as string}</p>
              )}
            </div>
          </div>
          )
        })}
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-sm text-white/30">Waiting for market data...</div>
        )}
        <div ref={bottomRef} />
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
