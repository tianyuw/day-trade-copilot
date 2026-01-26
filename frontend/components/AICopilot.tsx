"use client"

import { useEffect, useRef } from "react"
import { cn } from "./cn"

type AnalysisResult = {
  analysis_id: string
  timestamp: string
  symbol: string
  action: "buy_long" | "buy_short" | "ignore" | "follow_up" | "check_when_condition_meet"
  confidence: number
  reasoning: string
  pattern_name?: string | null
  breakout_price?: number | null
  watch_condition?: {
    trigger_price: number
    direction: "above" | "below"
    expiry_minutes: number
  } | null
  trade_plan?: {
    trade_id: string
    direction: "long" | "short"
    option: { right: "call" | "put"; expiration: string; strike: number }
    contracts: number
    risk?: { stop_loss_premium: number; time_stop_minutes: number }
    take_profit_premium?: number
    option_symbol?: string | null
  } | null
}

export type ChatMessage = {
  role: "ai" | "system"
  content: string | AnalysisResult
  time: string
  type?: "analysis" | "text"
  trigger_reason?: "quant_signal" | "follow_up" | "watch_condition" | "position_management"
}

export function AICopilot({ 
  symbol, 
  messages 
}: { 
  symbol: string
  messages: ChatMessage[]
}) {
  const bottomRef = useRef<HTMLDivElement>(null)

  const triggerLabel = (r: ChatMessage["trigger_reason"] | undefined) => {
    if (!r) return null
    if (r === "quant_signal") return "quant signal"
    if (r === "follow_up") return "follow up"
    if (r === "watch_condition") return "watch condition"
    if (r === "position_management") return "position management"
    return null
  }

  type MetaValue = string | number | null | undefined

  const metaLabels: Record<string, string> = {
    underlying_symbol: "Underlying Symbol",
    option_symbol: "Option Symbol",
    underlying_price: "Underlying Price",
    option_price: "Option Price",
    contracts: "Contracts",
    direction: "Direction",
    option: "Option",
    stop_loss: "Stop Loss",
    take_profit: "Take Profit",
    time_stop_minutes: "Time Stop",
    trade_id: "Trade ID",
  }

  const formatMetaValue = (key: string, value: MetaValue) => {
    if (value == null) return "N/A"
    const raw = String(value)
    if (!raw || raw === "N/A") return "N/A"
    if (key === "direction") return raw.toUpperCase()
    if (key === "time_stop_minutes") return `${raw}m`
    return raw
  }

  const renderMetaChips = (meta: Record<string, MetaValue>, keys: string[]) => {
    return (
      <div className="mb-3 flex flex-wrap gap-2">
        {keys.map((k) => (
          <div
            key={k}
            className="inline-flex items-center rounded-md bg-white/5 px-2 py-1 text-[10px] font-medium text-white/70 ring-1 ring-white/10"
          >
            <span className="mr-1 opacity-50">{(metaLabels[k] ?? k) + ":"}</span>
            {formatMetaValue(k, meta[k])}
          </div>
        ))}
      </div>
    )
  }

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

    const pick = (...keys: string[]) => {
      for (const k of keys) {
        const v = kv[k]
        if (v && v !== "N/A") return v
      }
      return null
    }

    const pmMeta: Record<string, MetaValue> = {
      underlying_symbol: pick("underlying_symbol") ?? symbol,
      option_symbol: pick("option_symbol"),
      underlying_price: pick("underlying_price", "last_px"),
      option_price: pick("option_price", "option_premium"),
      contracts: pick("contracts", "contracts_to_close"),
      direction: pick("direction"),
      option: pick("option"),
      stop_loss: pick("stop_loss", "stop_loss_premium", "new_stop"),
      take_profit: pick("take_profit", "take_profit_premium", "new_tp"),
      time_stop_minutes: pick("time_stop_minutes", "new_time_stop"),
    }

    const knownKeys = new Set([
      "underlying_symbol",
      "option_symbol",
      "underlying_price",
      "option_price",
      "contracts",
      "contracts_to_close",
      "direction",
      "option",
      "stop_loss",
      "stop_loss_premium",
      "new_stop",
      "take_profit",
      "take_profit_premium",
      "new_tp",
      "time_stop_minutes",
      "contracts_to_close",
      "new_time_stop",
      "last_px",
      "option_premium",
    ])
    const extraMeta = meta.filter((m) => {
      const idx = m.indexOf("=")
      if (idx <= 0) return true
      const k = m.slice(0, idx).trim()
      return !knownKeys.has(k)
    })

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
              trigger: position management
            </div>
          </div>
          <div className="text-xs font-mono text-white/40" />
        </div>
        {renderMetaChips(pmMeta, [
          "underlying_symbol",
          "underlying_price",
          "option_price",
          "contracts",
          "direction",
          "option",
          "option_symbol",
          "stop_loss",
          "take_profit",
          "time_stop_minutes",
        ])}

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
                        <div className="flex items-center gap-2">
                          {triggerLabel(msg.trigger_reason) ? (
                            <div className="px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-200 ring-1 ring-indigo-500/30">
                              trigger: {triggerLabel(msg.trigger_reason)}
                            </div>
                          ) : null}
                          <div className="text-xs font-mono text-white/40">
                              Conf: {(msg.content.confidence * 100).toFixed(0)}%
                          </div>
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
                                {renderMetaChips(
                                  {
                                    trade_id: msg.content.trade_plan.trade_id,
                                    underlying_symbol: msg.content.symbol,
                                    direction: msg.content.trade_plan.direction,
                                    contracts: msg.content.trade_plan.contracts,
                                    option: `${String(msg.content.trade_plan.option.right).toUpperCase()} ${msg.content.trade_plan.option.expiration} ${msg.content.trade_plan.option.strike}`,
                                    stop_loss: msg.content.trade_plan.risk?.stop_loss_premium,
                                    take_profit: msg.content.trade_plan.take_profit_premium,
                                    time_stop_minutes: msg.content.trade_plan.risk?.time_stop_minutes,
                                    option_symbol: msg.content.trade_plan.option_symbol ?? null,
                                  },
                                  [
                                    "trade_id",
                                    "underlying_symbol",
                                    "direction",
                                    "contracts",
                                    "option",
                                    "option_symbol",
                                    "stop_loss",
                                    "take_profit",
                                    "time_stop_minutes",
                                  ],
                                )}
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
