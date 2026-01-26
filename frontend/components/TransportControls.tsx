"use client"

type Props = {
  mode: "playback" | "realtime" | "readonly"
  startLocal: string
  onStartLocalChange: (v: string) => void
  isPlaying: boolean
  onTogglePlay: () => void
  onReset: () => void
}

export function TransportControls({ mode, startLocal, onStartLocalChange, isPlaying, onTogglePlay, onReset }: Props) {
  if (mode !== "playback") return null

  return (
    <div className="flex flex-wrap items-center gap-4">
      <div className="flex items-center gap-3 rounded-xl bg-black/40 px-4 py-2 ring-1 ring-white/10">
        <span className="text-xs font-bold text-white/40 uppercase">Start Time (PT)</span>
        <input
          type="datetime-local"
          value={startLocal}
          onChange={(e) => onStartLocalChange(e.target.value)}
          className="bg-transparent text-sm font-mono font-medium text-white outline-none focus:text-cyan-300 [&::-webkit-calendar-picker-indicator]:invert [&::-webkit-calendar-picker-indicator]:opacity-50 hover:[&::-webkit-calendar-picker-indicator]:opacity-100"
        />
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={onTogglePlay}
          className={`flex items-center gap-2 rounded-xl px-6 py-2.5 text-sm font-bold transition-all ${
            isPlaying
              ? "bg-amber-500/20 text-amber-300 ring-1 ring-amber-500/50 hover:bg-amber-500/30"
              : "bg-white text-black hover:bg-cyan-50 hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]"
          }`}
        >
          {isPlaying ? (
            <>
              <svg className="h-4 w-4 fill-current" viewBox="0 0 24 24">
                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
              </svg>
              Pause
            </>
          ) : (
            <>
              <svg className="h-4 w-4 fill-current" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
              Start Replay
            </>
          )}
        </button>

        <button
          onClick={onReset}
          className="rounded-xl bg-white/5 p-2.5 text-white/70 ring-1 ring-white/10 hover:bg-white/10 hover:text-white transition-colors"
          title="Reset"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
        </button>
      </div>
    </div>
  )
}

