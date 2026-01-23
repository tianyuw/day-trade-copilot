"use client"

import { useEffect, useMemo, useState } from "react"

import { cn } from "./cn"

type Execution = "paper" | "live"

export function TradingPanel() {
  const [open, setOpen] = useState(false)
  const [execution, setExecution] = useState<Execution>("paper")
  const [positions, setPositions] = useState<any[]>([])
  const [orders, setOrders] = useState<any[]>([])
  const [activities, setActivities] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const baseHttp = useMemo(() => {
    if (typeof window === "undefined") return ""
    return process.env.NEXT_PUBLIC_BACKEND_API ?? `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
  }, [])

  useEffect(() => {
    if (typeof window === "undefined") return
    const rawExec = window.localStorage.getItem("defaultExecution")
    if (rawExec === "paper" || rawExec === "live") setExecution(rawExec)
  }, [])

  const refresh = async () => {
    if (!baseHttp) return
    setLoading(true)
    setError(null)
    try {
      const [p, o, a] = await Promise.all([
        fetch(`${baseHttp}/api/trading/positions?execution=${execution}`).then((r) => r.json()),
        fetch(`${baseHttp}/api/trading/orders?execution=${execution}&status=open&limit=50`).then((r) => r.json()),
        fetch(`${baseHttp}/api/trading/activities?execution=${execution}&page_size=50`).then((r) => r.json()),
      ])
      setPositions(Array.isArray(p?.positions) ? p.positions : [])
      setOrders(Array.isArray(o?.orders) ? o.orders : [])
      setActivities(Array.isArray(a?.activities) ? a.activities : [])
    } catch {
      setError("Failed to load trading data.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!open) return
    refresh()
  }, [open, execution])

  return (
    <div className="fixed bottom-5 right-5 z-40">
      {open ? (
        <div className="w-[420px] rounded-2xl bg-black/50 p-4 ring-1 ring-white/10 backdrop-blur-xl shadow-[0_0_40px_rgba(0,0,0,0.7)]">
          <div className="flex items-center justify-between gap-3">
            <div className="text-sm font-semibold text-white/90">Trading</div>
            <div className="flex items-center gap-2">
              <div className="inline-flex items-center gap-1 rounded-xl bg-white/5 p-1 ring-1 ring-white/10">
                <button
                  type="button"
                  onClick={() => setExecution("paper")}
                  className={cn(
                    "rounded-lg px-2.5 py-1 text-[11px] font-semibold transition",
                    execution === "paper" ? "bg-white text-black" : "text-white/70 hover:bg-white/10",
                  )}
                >
                  Paper
                </button>
                <button
                  type="button"
                  onClick={() => setExecution("live")}
                  className={cn(
                    "rounded-lg px-2.5 py-1 text-[11px] font-semibold transition",
                    execution === "live" ? "bg-red-500 text-white" : "text-white/70 hover:bg-white/10",
                  )}
                >
                  Live
                </button>
              </div>
              <button
                type="button"
                onClick={refresh}
                disabled={loading}
                className="rounded-xl bg-white/5 px-3 py-1.5 text-[11px] font-semibold text-white/80 ring-1 ring-white/10 transition hover:bg-white/10 disabled:opacity-60"
              >
                Refresh
              </button>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="rounded-xl bg-white/5 px-3 py-1.5 text-[11px] font-semibold text-white/80 ring-1 ring-white/10 transition hover:bg-white/10"
              >
                Close
              </button>
            </div>
          </div>

          {error ? <div className="mt-3 text-xs text-rose-300">{error}</div> : null}

          <div className="mt-4 space-y-3 text-xs">
            <div className="rounded-xl bg-white/5 p-3 ring-1 ring-white/10">
              <div className="font-semibold text-white/80 mb-2">Positions ({positions.length})</div>
              <div className="max-h-36 overflow-auto space-y-1 text-white/70 font-mono">
                {positions.map((p) => (
                  <div key={String(p?.symbol ?? Math.random())} className="flex justify-between gap-3">
                    <div className="truncate">{String(p?.symbol ?? "")}</div>
                    <div className="flex-none opacity-70">{String(p?.qty ?? "")}</div>
                  </div>
                ))}
                {positions.length === 0 ? <div className="text-white/40">No open positions</div> : null}
              </div>
            </div>

            <div className="rounded-xl bg-white/5 p-3 ring-1 ring-white/10">
              <div className="font-semibold text-white/80 mb-2">Open Orders ({orders.length})</div>
              <div className="max-h-36 overflow-auto space-y-1 text-white/70 font-mono">
                {orders.map((o) => (
                  <div key={String(o?.id ?? Math.random())} className="flex justify-between gap-3">
                    <div className="truncate">{String(o?.symbol ?? "")}</div>
                    <div className="flex-none opacity-70">{String(o?.side ?? "")} {String(o?.qty ?? "")}</div>
                  </div>
                ))}
                {orders.length === 0 ? <div className="text-white/40">No open orders</div> : null}
              </div>
            </div>

            <div className="rounded-xl bg-white/5 p-3 ring-1 ring-white/10">
              <div className="font-semibold text-white/80 mb-2">Recent Activities ({activities.length})</div>
              <div className="max-h-36 overflow-auto space-y-1 text-white/70 font-mono">
                {activities.map((a) => (
                  <div key={String(a?.id ?? Math.random())} className="flex justify-between gap-3">
                    <div className="truncate">{String(a?.symbol ?? "")}</div>
                    <div className="flex-none opacity-70">{String(a?.activity_type ?? "")}</div>
                  </div>
                ))}
                {activities.length === 0 ? <div className="text-white/40">No recent activities</div> : null}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="rounded-2xl bg-white/10 px-4 py-3 text-xs font-bold text-white/80 ring-1 ring-white/15 backdrop-blur-xl transition hover:bg-white/15 hover:ring-white/25"
        >
          Trading
        </button>
      )}
    </div>
  )
}

