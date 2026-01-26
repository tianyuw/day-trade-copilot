"use client"

import { useMemo } from "react"

export function useBackendBaseUrls(): { baseHttp: string; baseWs: string } {
  const baseHttp = useMemo(() => {
    if (typeof window === "undefined") return ""
    return (
      process.env.NEXT_PUBLIC_BACKEND_API ??
      `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
    )
  }, [])

  const baseWs = useMemo(() => {
    if (typeof window === "undefined") return ""
    return process.env.NEXT_PUBLIC_BACKEND_WS ?? `ws://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_WS_PORT ?? "8000"}`
  }, [])

  return { baseHttp, baseWs }
}

