"use client"

import { cn } from "./cn"

export type Segment<T extends string> = { value: T; label: string }

export function Segmented<T extends string>({
  value,
  onChange,
  segments,
  className,
}: {
  value: T
  onChange: (v: T) => void
  segments: Segment<T>[]
  className?: string
}) {
  return (
    <div className={cn("flex rounded-2xl bg-white/8 p-1 ring-1 ring-white/10 backdrop-blur-md", className)}>
      {segments.map((s) => {
        const active = s.value === value
        return (
          <button
            key={s.value}
            onClick={() => onChange(s.value)}
            className={cn(
              "flex-1 rounded-2xl px-3 py-2 text-xs font-semibold transition",
              active ? "bg-white/12 text-white shadow-neo" : "text-white/70 hover:text-white",
            )}
          >
            {s.label}
          </button>
        )
      })}
    </div>
  )
}

