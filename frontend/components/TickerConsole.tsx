"use client"

import type { ReactNode } from "react"
import { AICopilot, type ChatMessage } from "./AICopilot"
import { CandleCard } from "./CandleCard"
import { cn } from "./cn"

export function TickerConsole({
  headerLeft,
  headerRight,
  notice,
  symbol,
  bars,
  prevClose,
  chartStatus,
  isAnalyzing,
  onPause,
  onResume,
  onAnalyze,
  aiMessages,
  hideAIPanelOnSmall = true,
}: {
  headerLeft: ReactNode
  headerRight?: ReactNode
  notice?: ReactNode
  symbol: string
  bars: any[]
  prevClose?: number | null
  chartStatus?: "hot" | "watch" | "normal"
  isAnalyzing?: boolean
  onPause?: () => void
  onResume?: () => void
  onAnalyze?: (time: string) => Promise<void>
  aiMessages: ChatMessage[]
  hideAIPanelOnSmall?: boolean
}) {
  return (
    <main className="flex h-screen flex-col bg-neon-radial text-white font-sans overflow-hidden">
      <div className="flex-none border-b border-white/10 bg-black/20 backdrop-blur-xl px-6 py-4">
        <div className="mx-auto flex max-w-[1600px] flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="min-w-0">{headerLeft}</div>
          {headerRight ? <div className="flex flex-wrap items-center gap-4">{headerRight}</div> : null}
        </div>
        {notice ? <div className="mx-auto mt-3 max-w-[1600px]">{notice}</div> : null}
      </div>

      <div className="flex-1 min-h-0 p-6 overflow-hidden">
        <div className="mx-auto flex h-full min-h-0 max-w-[1600px] flex-col gap-6">
          <div className={cn("grid flex-1 min-h-0 gap-6", "grid-cols-1", "lg:grid-cols-[2fr_1fr]")}>
            <div className="min-w-0 h-full min-h-0">
              <div className="relative h-full rounded-3xl bg-black/40 shadow-neo ring-1 ring-white/10 backdrop-blur-md overflow-hidden p-1">
                <CandleCard
                  symbol={symbol}
                  bars={bars}
                  prevClose={prevClose}
                  className="h-full w-full !bg-transparent !shadow-none !ring-0 !backdrop-blur-none"
                  status={chartStatus}
                  isAnalyzing={isAnalyzing}
                  onPause={onPause}
                  onResume={onResume}
                  onAnalyze={onAnalyze}
                />
              </div>
            </div>

            <div className={cn("h-full min-w-0 min-h-0", hideAIPanelOnSmall ? "hidden lg:block" : "")}>
              <AICopilot symbol={symbol} messages={aiMessages} />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

