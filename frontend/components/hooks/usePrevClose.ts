"use client"

import { useEffect, useState } from "react"

export function usePrevClose(
  baseHttp: string,
  symbol: string,
  opts?: { asof?: string | null; enabled?: boolean },
): { prevClose: number | null; prevCloseError: string | null } {
  const enabled = opts?.enabled ?? true
  const asof = opts?.asof ?? null

  const [prevClose, setPrevClose] = useState<number | null>(null)
  const [prevCloseError, setPrevCloseError] = useState<string | null>(null)

  useEffect(() => {
    if (!enabled) return
    if (!baseHttp) return
    if (!symbol) return

    let cancelled = false

    async function fetchPrevClose() {
      try {
        const q = new URLSearchParams()
        q.set("symbols", symbol)
        if (asof) q.set("asof", asof)
        const res = await fetch(`${baseHttp}/api/stocks/prev_close?${q.toString()}`)
        if (!res.ok) throw new Error("prev_close failed")
        const data = await res.json()
        const v = data?.prev_close?.[symbol]
        if (cancelled) return
        setPrevClose(typeof v === "number" ? v : null)
        setPrevCloseError(null)
      } catch (e) {
        if (cancelled) return
        setPrevClose(null)
        setPrevCloseError(e instanceof Error ? e.message : "prev_close failed")
      }
    }

    fetchPrevClose()
    return () => {
      cancelled = true
    }
  }, [asof, baseHttp, enabled, symbol])

  return { prevClose, prevCloseError }
}

