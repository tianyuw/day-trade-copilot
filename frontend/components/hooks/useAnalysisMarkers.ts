"use client"

import { useCallback, useRef } from "react"

function toUtcMinuteEpoch(rfc3339: string): number | null {
  const ms = new Date(rfc3339).getTime()
  if (!Number.isFinite(ms)) return null
  return Math.floor(ms / 1000 / 60) * 60
}

export function useAnalysisMarkers(): {
  recordAnalysisMarker: (ts: string, payload: any) => void
  applyMarkersToBars: <T extends Record<string, any>>(bars: T[]) => T[]
  clearMarkers: () => void
} {
  const markerByMinuteRef = useRef<Map<number, true>>(new Map())

  const recordAnalysisMarker = useCallback((ts: string, payload: any) => {
    const minute = toUtcMinuteEpoch(ts)
    if (minute == null) return
    markerByMinuteRef.current.set(minute, true)
  }, [])

  const applyMarkersToBars = useCallback(<T extends Record<string, any>>(barsIn: T[]) => {
    if (!Array.isArray(barsIn) || barsIn.length === 0) return barsIn
    const markers = markerByMinuteRef.current
    if (markers.size === 0) return barsIn

    return barsIn.map((b) => {
      const t = typeof b?.t === "string" ? b.t : ""
      const minute = t ? toUtcMinuteEpoch(t) : null
      if (minute == null) return b
      if (!markers.has(minute)) return b
      if ((b as any)?.ui_marker) return b
      const o = typeof (b as any)?.o === "number" ? Number((b as any).o) : null
      const c = typeof (b as any)?.c === "number" ? Number((b as any).c) : null
      const color: "green" | "red" =
        typeof o === "number" && typeof c === "number" && c >= o ? "green" : "red"
      return { ...b, ui_marker: { color, kind: "analysis" } }
    })
  }, [])

  const clearMarkers = useCallback(() => {
    markerByMinuteRef.current.clear()
  }, [])

  return { recordAnalysisMarker, applyMarkersToBars, clearMarkers }
}
