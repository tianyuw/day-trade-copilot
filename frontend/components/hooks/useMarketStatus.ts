"use client"

import { useEffect, useState } from "react"

export type MarketStatus = {
  server_time: string
  session: "pre_market" | "regular" | "after_hours" | "closed"
  is_open: boolean
  next_open: string
  next_close: string
  last_rth_open?: string
  last_rth_close?: string
}

function isSameMarketCore(a: MarketStatus, b: MarketStatus): boolean {
  return (
    a.session === b.session &&
    a.is_open === b.is_open &&
    a.next_open === b.next_open &&
    a.next_close === b.next_close &&
    (a.last_rth_open ?? null) === (b.last_rth_open ?? null) &&
    (a.last_rth_close ?? null) === (b.last_rth_close ?? null)
  )
}

export function useMarketStatus(
  baseHttp: string,
  opts?: { pollMs?: number; enabled?: boolean },
): { market: MarketStatus | null; marketError: string | null } {
  const pollMs = opts?.pollMs ?? 30_000
  const enabled = opts?.enabled ?? true

  const [market, setMarket] = useState<MarketStatus | null>(null)
  const [marketError, setMarketError] = useState<string | null>(null)

  useEffect(() => {
    if (!enabled) return
    if (!baseHttp) return

    let cancelled = false

    async function fetchMarket() {
      try {
        const res = await fetch(`${baseHttp}/api/market/status`)
        if (!res.ok) throw new Error("market status failed")
        const data = (await res.json()) as MarketStatus
        if (cancelled) return
        setMarket((prev) => {
          if (prev && isSameMarketCore(prev, data)) return prev
          return data
        })
        setMarketError(null)
      } catch (e) {
        if (cancelled) return
        setMarket(null)
        setMarketError(e instanceof Error ? e.message : "market status failed")
      }
    }

    fetchMarket()
    const t = window.setInterval(fetchMarket, pollMs)
    return () => {
      cancelled = true
      window.clearInterval(t)
    }
  }, [baseHttp, enabled, pollMs])

  return { market, marketError }
}
