"use client"

import { useEffect, useRef, useState } from "react"
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
            <p className="text-xs text-white/50">Realtime Analysis</p>
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
            <div className="space-y-1 w-full min-w-0">
              <div className="text-xs font-mono text-white/30">{msg.time}</div>
              
              {msg.type === "analysis" && typeof msg.content === 'object' ? (
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
                </div>
              ) : (
                <p className="text-sm leading-relaxed text-white/90 whitespace-pre-wrap">{msg.content as string}</p>
              )}
            </div>
          </div>
        ))}
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
