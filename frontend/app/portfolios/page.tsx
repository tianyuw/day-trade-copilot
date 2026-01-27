"use client"

import Link from "next/link"
import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { ArrowUpRight, RefreshCw, Search } from "lucide-react"
import { cn } from "../../components/cn"
import { useBackendBaseUrls } from "../../components/hooks/useBackendBaseUrls"

type TradingExecution = "paper" | "live"

type TradingSettings = {
  auto_trade_execution_enabled?: boolean
  live_trading_enabled?: boolean
  default_execution?: TradingExecution
}

type AlpacaAccount = Record<string, unknown> & {
  equity?: string
  portfolio_value?: string
  buying_power?: string
  cash?: string
  cash_withdrawable?: string
  last_equity?: string
}

type AlpacaPosition = Record<string, unknown> & {
  symbol?: string
  asset_class?: string
  qty?: string
  avg_entry_price?: string
  current_price?: string
  lastday_price?: string
  market_value?: string
  cost_basis?: string
  unrealized_pl?: string
  unrealized_plpc?: string
  unrealized_intraday_pl?: string
  unrealized_intraday_plpc?: string
  change_today?: string
}

type PortfolioHistory = {
  timestamp?: number[]
  equity?: number[]
}

function toNumber(v: unknown): number | null {
  if (typeof v === "number") return Number.isFinite(v) ? v : null
  if (typeof v === "string") {
    const n = Number(v)
    return Number.isFinite(n) ? n : null
  }
  return null
}

function formatMoney(v: number | null, currency: string = "USD"): string {
  if (v === null || !Number.isFinite(v)) return "—"
  try {
    return new Intl.NumberFormat("en-US", { style: "currency", currency, maximumFractionDigits: 2 }).format(v)
  } catch {
    return `$${v.toFixed(2)}`
  }
}

function formatPct(v: number | null): string {
  if (v === null || !Number.isFinite(v)) return "—"
  try {
    return new Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2 }).format(v)
  } catch {
    return `${(v * 100).toFixed(2)}%`
  }
}

function pnlClass(v: number | null): string {
  if (v === null || !Number.isFinite(v) || v === 0) return "text-white/70"
  return v > 0 ? "text-emerald-300" : "text-rose-300"
}

function isLikelyOption(p: AlpacaPosition): boolean {
  const ac = String(p.asset_class ?? "").toLowerCase()
  if (ac.includes("option")) return true
  const sym = String(p.symbol ?? "")
  return sym.includes(" ") || sym.includes(":")
}

function buildLinePath(values: number[], width: number, height: number): string {
  if (values.length < 2) return ""
  const min = Math.min(...values)
  const max = Math.max(...values)
  const span = max - min || 1
  const padX = 2
  const padY = 6
  const w = Math.max(1, width - padX * 2)
  const h = Math.max(1, height - padY * 2)
  const pts = values.map((v, i) => {
    const x = padX + (i / (values.length - 1)) * w
    const y = padY + (1 - (v - min) / span) * h
    return [x, y] as const
  })
  return `M ${pts[0][0].toFixed(2)} ${pts[0][1].toFixed(2)} ${pts
    .slice(1)
    .map(([x, y]) => `L ${x.toFixed(2)} ${y.toFixed(2)}`)
    .join(" ")}`
}

export default function PortfoliosPage() {
  const { baseHttp } = useBackendBaseUrls()

  const [settings, setSettings] = useState<TradingSettings | null>(null)
  const [execution, setExecution] = useState<TradingExecution>("paper")

  const [account, setAccount] = useState<AlpacaAccount | null>(null)
  const [positions, setPositions] = useState<AlpacaPosition[]>([])
  const [history, setHistory] = useState<PortfolioHistory | null>(null)

  const [view, setView] = useState<"all" | "stocks" | "options">("all")
  const [symbolFilter, setSymbolFilter] = useState("")
  const [sortKey, setSortKey] = useState<"market_value" | "unrealized_pl" | "day_pl" | "nav_pct">("market_value")

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const lastUpdatedRef = useRef<number | null>(null)

  useEffect(() => {
    if (!baseHttp) return
    const controller = new AbortController()
    ;(async () => {
      try {
        const res = await fetch(`${baseHttp}/api/settings/trading`, { method: "GET", signal: controller.signal })
        if (!res.ok) throw new Error("settings_failed")
        const data = (await res.json()) as TradingSettings
        setSettings(data)
        if (data.default_execution === "paper" || data.default_execution === "live") {
          setExecution(data.default_execution)
        }
      } catch {
        if (!controller.signal.aborted) setSettings(null)
      }
    })()
    return () => controller.abort()
  }, [baseHttp])

  const refresh = useCallback(async (targetExecution: TradingExecution) => {
    if (!baseHttp) return
    setIsLoading(true)
    setError(null)
    try {
      const [settingsRes, accRes, posRes, histRes] = await Promise.all([
        fetch(`${baseHttp}/api/settings/trading`, { method: "GET" }),
        fetch(`${baseHttp}/api/trading/account?execution=${encodeURIComponent(targetExecution)}`, {
          method: "GET",
        }),
        fetch(`${baseHttp}/api/trading/positions?execution=${encodeURIComponent(targetExecution)}`, {
          method: "GET",
        }),
        fetch(`${baseHttp}/api/trading/portfolio_history?execution=${encodeURIComponent(targetExecution)}&period=1D&timeframe=1Min`, {
          method: "GET",
        }),
      ])

      if (settingsRes.ok) {
        const s = (await settingsRes.json()) as TradingSettings
        setSettings(s)
        const liveEnabled = Boolean(s?.live_trading_enabled)
        if (targetExecution === "live" && !liveEnabled) {
          setExecution("paper")
          setError("Live trading is disabled on the server.")
          return
        }
      }

      if (accRes.status === 403 && targetExecution === "live") {
        setExecution("paper")
        setError("Live trading is disabled on the server.")
        return
      }
      if (!accRes.ok) throw new Error("account_failed")
      if (!posRes.ok) throw new Error("positions_failed")

      const acc = (await accRes.json()) as AlpacaAccount
      const posPayload = (await posRes.json()) as { positions?: unknown }
      const pos = Array.isArray(posPayload?.positions) ? (posPayload.positions as AlpacaPosition[]) : []

      let hist: PortfolioHistory | null = null
      if (histRes.ok) {
        const raw = (await histRes.json()) as PortfolioHistory
        hist = raw
      }

      setAccount(acc)
      setPositions(pos)
      setHistory(hist)
      lastUpdatedRef.current = Date.now()
    } catch {
      setError("Failed to load portfolio data.")
    } finally {
      setIsLoading(false)
    }
  }, [baseHttp])

  useEffect(() => {
    void refresh(execution)
  }, [execution, refresh])

  const nav = useMemo(() => {
    const v = toNumber(account?.portfolio_value) ?? toNumber(account?.equity)
    return v
  }, [account])

  const cashBuyingPower = useMemo(() => {
    return toNumber(account?.buying_power) ?? toNumber(account?.cash)
  }, [account])

  const availableForWithdrawal = useMemo(() => {
    return toNumber(account?.cash_withdrawable) ?? toNumber(account?.cash)
  }, [account])

  const totals = useMemo(() => {
    let marketValue = 0
    let costBasis = 0
    let unrealized = 0
    let dayUnrealized = 0

    for (const p of positions) {
      const mv = toNumber(p.market_value) ?? 0
      const cb = toNumber(p.cost_basis) ?? 0
      const upl = toNumber(p.unrealized_pl) ?? 0
      const uipl = toNumber(p.unrealized_intraday_pl)

      marketValue += mv
      costBasis += cb
      unrealized += upl

      if (uipl !== null) {
        dayUnrealized += uipl
        continue
      }

      const qty = toNumber(p.qty)
      const current = toNumber(p.current_price)
      const lastday = toNumber(p.lastday_price)
      if (qty !== null && current !== null && lastday !== null) {
        dayUnrealized += (current - lastday) * qty
      }
    }

    const unrealizedPct = costBasis > 0 ? unrealized / costBasis : null
    const dayUnrealizedPct = costBasis > 0 ? dayUnrealized / costBasis : null
    return { marketValue, costBasis, unrealized, unrealizedPct, dayUnrealized, dayUnrealizedPct }
  }, [positions])

  const dayTotalGain = useMemo(() => {
    const eq = history?.equity ?? []
    if (eq.length < 2) return null
    const first = eq[0]
    const last = eq[eq.length - 1]
    if (!Number.isFinite(first) || !Number.isFinite(last) || first === 0) return null
    return { usd: last - first, pct: (last - first) / first }
  }, [history])

  const dayRealized = useMemo(() => {
    if (!dayTotalGain) return null
    return dayTotalGain.usd - totals.dayUnrealized
  }, [dayTotalGain, totals.dayUnrealized])

  const dayRealizedPct = useMemo(() => {
    if (dayRealized === null) return null
    if (!totals.costBasis || totals.costBasis <= 0) return null
    return dayRealized / totals.costBasis
  }, [dayRealized, totals.costBasis])

  const equityPath = useMemo(() => {
    const eq = history?.equity ?? []
    if (eq.length < 2) return ""
    return buildLinePath(eq.slice(-120), 420, 120)
  }, [history])

  const filteredPositions = useMemo(() => {
    const q = symbolFilter.trim().toUpperCase()
    let list = positions
    if (view !== "all") {
      const wantOptions = view === "options"
      list = list.filter((p) => isLikelyOption(p) === wantOptions)
    }
    if (q) {
      list = list.filter((p) => String(p.symbol ?? "").toUpperCase().includes(q))
    }
    const rows = [...list]
    const getDayPl = (p: AlpacaPosition): number => {
      const uipl = toNumber(p.unrealized_intraday_pl)
      if (uipl !== null) return uipl
      const qty = toNumber(p.qty)
      const current = toNumber(p.current_price)
      const lastday = toNumber(p.lastday_price)
      if (qty !== null && current !== null && lastday !== null) return (current - lastday) * qty
      return 0
    }
    const getNavPct = (p: AlpacaPosition): number => {
      const mv = toNumber(p.market_value) ?? 0
      if (!nav || nav === 0) return 0
      return mv / nav
    }
    rows.sort((a, b) => {
      if (sortKey === "market_value") return (toNumber(b.market_value) ?? 0) - (toNumber(a.market_value) ?? 0)
      if (sortKey === "unrealized_pl") return (toNumber(b.unrealized_pl) ?? 0) - (toNumber(a.unrealized_pl) ?? 0)
      if (sortKey === "day_pl") return getDayPl(b) - getDayPl(a)
      return getNavPct(b) - getNavPct(a)
    })
    return rows
  }, [positions, view, symbolFilter, sortKey, nav])

  const tableTotals = useMemo(() => {
    let marketValue = 0
    let unrealized = 0
    let dayPl = 0
    for (const p of filteredPositions) {
      marketValue += toNumber(p.market_value) ?? 0
      unrealized += toNumber(p.unrealized_pl) ?? 0
      const uipl = toNumber(p.unrealized_intraday_pl)
      if (uipl !== null) {
        dayPl += uipl
      } else {
        const qty = toNumber(p.qty)
        const current = toNumber(p.current_price)
        const lastday = toNumber(p.lastday_price)
        if (qty !== null && current !== null && lastday !== null) dayPl += (current - lastday) * qty
      }
    }
    return { marketValue, unrealized, dayPl }
  }, [filteredPositions])

  const lastUpdatedLabel = useMemo(() => {
    const ts = lastUpdatedRef.current
    if (!ts) return ""
    try {
      return new Intl.DateTimeFormat("en-US", { hour: "2-digit", minute: "2-digit", second: "2-digit" }).format(new Date(ts))
    } catch {
      return ""
    }
  }, [isLoading, account, positions.length])

  const liveSelectable = Boolean(settings?.live_trading_enabled)

  return (
    <main className="flex min-h-screen flex-col bg-neon-radial text-white font-sans">
      <div className="sticky top-0 z-40 flex-none border-b border-white/10 bg-black/20 backdrop-blur-xl">
        <div className="px-6 py-4">
          <div className="mx-auto flex max-w-[1600px] flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-tr from-cyan-500/20 to-purple-500/20 ring-1 ring-white/10 shadow-[0_0_15px_rgba(34,211,238,0.18)]">
                  <svg className="h-5 w-5 text-cyan-300" aria-hidden="true">
                    <use href="#icon-trend" />
                  </svg>
                </div>
                <div className="min-w-0">
                  <div className="text-xs font-medium text-white/40 uppercase tracking-wider">Portfolios</div>
                  <div className="truncate text-base font-extrabold tracking-tight">Account Overview</div>
                </div>
              </div>

              <div className="h-8 w-px bg-white/10 hidden lg:block" />

              <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-2 text-xs font-semibold text-white/70 ring-1 ring-white/10">
                <span className="text-white/40">Account</span>
                <select
                  className="bg-transparent text-white/90 outline-none"
                  value={execution}
                  onChange={(e) => {
                    const v = e.target.value
                    if (v === "paper" || v === "live") setExecution(v)
                  }}
                  aria-label="Select account execution"
                >
                  <option value="paper">Paper Trading</option>
                  <option value="live" disabled={!liveSelectable}>
                    Individual Trading{liveSelectable ? "" : " (Disabled)"}
                  </option>
                  <option value="brokerage" disabled>
                    Brokerage Accounts (Coming Soon)
                  </option>
                </select>
              </div>

              <div className="hidden sm:flex items-center gap-2 rounded-full bg-white/5 px-3 py-2 text-xs font-semibold text-white/60 ring-1 ring-white/10">
                <span className="text-white/40">Data</span>
                <span>{isLoading ? "Loading" : error ? "Error" : "Realtime"}</span>
                {lastUpdatedLabel ? <span className="text-white/40">· {lastUpdatedLabel}</span> : null}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                className="inline-flex items-center gap-2 rounded-2xl bg-white/5 px-4 py-2 text-sm font-bold text-white/80 ring-1 ring-white/10 transition hover:bg-white/10 hover:ring-white/20 focus:outline-none focus:ring-2 focus:ring-cyan-400/70 disabled:opacity-50"
                onClick={() => void refresh(execution)}
                disabled={isLoading || !baseHttp}
              >
                <RefreshCw className={cn("h-4 w-4", isLoading ? "animate-spin" : "")} aria-hidden="true" />
                Refresh
              </button>

              <Link
                href="/tracking"
                className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-cyan-300/15 to-purple-300/15 px-4 py-2 text-sm font-bold text-white ring-1 ring-white/10 transition hover:from-cyan-300/25 hover:to-purple-300/25 focus:outline-none focus:ring-2 focus:ring-cyan-400/70"
              >
                Open Tracking
                <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
              </Link>
            </div>
          </div>
        </div>

        {error ? (
          <div className="px-6 pb-4">
            <div className="mx-auto max-w-[1600px] rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
              {error}
            </div>
          </div>
        ) : null}
      </div>

      <div className="mx-auto w-full max-w-[1600px] flex-1 px-6 py-6">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          <section className="lg:col-span-12">
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
              <div className="lg:col-span-8 rounded-[26px] border border-white/10 bg-white/5 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] overflow-hidden">
                <div className="flex items-center justify-between px-5 py-4">
                  <div className="min-w-0">
                    <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Equity Curve (Today)</div>
                    <div className="mt-1 flex items-baseline gap-3">
                      <div className="text-2xl font-black tracking-tight">{formatMoney(nav)}</div>
                      <div className={cn("text-sm font-bold", pnlClass(dayTotalGain?.usd ?? null))}>
                        {dayTotalGain ? `${formatMoney(dayTotalGain.usd)} (${formatPct(dayTotalGain.pct)})` : "—"}
                      </div>
                    </div>
                  </div>
                  <div className="text-xs font-semibold text-white/50">NAV</div>
                </div>
                <div className="px-5 pb-5">
                  <div className="rounded-[22px] border border-white/10 bg-white/5 p-3">
                    <svg viewBox="0 0 420 120" className="h-[120px] w-full" role="img" aria-label="Equity curve">
                      <defs>
                        <linearGradient id="eqStroke" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#67E8F9" stopOpacity="0.95" />
                          <stop offset="55%" stopColor="#A78BFA" stopOpacity="0.95" />
                          <stop offset="100%" stopColor="#FDE68A" stopOpacity="0.9" />
                        </linearGradient>
                      </defs>
                      {equityPath ? (
                        <path
                          d={equityPath}
                          fill="none"
                          stroke="url(#eqStroke)"
                          strokeWidth="3"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          style={{
                            strokeDasharray: 900,
                            strokeDashoffset: 900,
                            animation: "dash 1200ms ease forwards",
                          }}
                        />
                      ) : (
                        <path d="M 2 70 L 120 64 L 230 78 L 330 58 L 418 66" fill="none" stroke="url(#eqStroke)" strokeWidth="3" opacity="0.35" />
                      )}
                    </svg>
                  </div>
                  <style jsx>{`
                    @keyframes dash {
                      to {
                        stroke-dashoffset: 0;
                      }
                    }
                  `}</style>
                </div>
              </div>

              <div className="lg:col-span-4 grid grid-cols-2 gap-4">
                <div className="rounded-[26px] border border-white/10 bg-white/5 p-4 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] transition hover:filter hover:drop-shadow(0_0_18px_rgba(139,92,246,0.45))">
                  <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Total Unrealized Gain</div>
                  <div className={cn("mt-2 text-lg font-black", pnlClass(totals.unrealized))}>{formatMoney(totals.unrealized)}</div>
                  <div className="mt-1 text-xs font-semibold text-white/50">{formatPct(totals.unrealizedPct)}</div>
                </div>

                <div className="rounded-[26px] border border-white/10 bg-white/5 p-4 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] transition hover:filter hover:drop-shadow(0_0_18px_rgba(34,211,238,0.35))">
                  <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Day's Gain Unrealized</div>
                  <div className={cn("mt-2 text-lg font-black", pnlClass(totals.dayUnrealized))}>{formatMoney(totals.dayUnrealized)}</div>
                  <div className="mt-1 text-xs font-semibold text-white/50">{formatPct(totals.dayUnrealizedPct)}</div>
                </div>

                <div className="rounded-[26px] border border-white/10 bg-white/5 p-4 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] transition hover:filter hover:drop-shadow(0_0_18px_rgba(251,113,133,0.25))">
                  <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Day's Gain Realized</div>
                  <div className={cn("mt-2 text-lg font-black", pnlClass(dayRealized))}>{formatMoney(dayRealized)}</div>
                  <div className="mt-1 text-xs font-semibold text-white/50">{formatPct(dayRealizedPct)}</div>
                </div>

                <div className="rounded-[26px] border border-white/10 bg-white/5 p-4 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] transition hover:filter hover:drop-shadow(0_0_18px_rgba(253,224,71,0.18))">
                  <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Cash Purchasing Power</div>
                  <div className="mt-2 text-lg font-black text-white/90">{formatMoney(cashBuyingPower)}</div>
                  <div className="mt-1 text-xs font-semibold text-white/50">Buying Power</div>
                </div>

                <div className="col-span-2 rounded-[26px] border border-white/10 bg-white/5 p-4 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] transition hover:filter hover:drop-shadow(0_0_18px_rgba(59,130,246,0.22))">
                  <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Available for Withdrawl</div>
                  <div className="mt-2 text-lg font-black text-white/90">{formatMoney(availableForWithdrawal)}</div>
                  <div className="mt-1 text-xs font-semibold text-white/50">{toNumber(account?.cash_withdrawable) !== null ? "Cash withdrawable" : "Estimate"}</div>
                </div>
              </div>
            </div>
          </section>

          <section className="lg:col-span-12">
            <div className="rounded-[26px] border border-white/10 bg-white/5 backdrop-blur-xl shadow-[inset_10px_10px_18px_rgba(0,0,0,0.55),inset_-10px_-10px_18px_rgba(255,255,255,0.06)] overflow-hidden">
              <div className="flex flex-col gap-3 px-5 py-4 lg:flex-row lg:items-center lg:justify-between">
                <div className="flex flex-wrap items-center gap-2">
                  <div className="text-xs font-semibold text-white/50 uppercase tracking-wider">Positions</div>

                  <div className="ml-0 flex items-center gap-2 rounded-full bg-white/5 px-3 py-2 text-xs font-semibold text-white/70 ring-1 ring-white/10">
                    <span className="text-white/40">View</span>
                    <select
                      className="bg-transparent text-white/90 outline-none"
                      value={view}
                      onChange={(e) => setView(e.target.value as any)}
                      aria-label="Select view"
                    >
                      <option value="all">All Positions</option>
                      <option value="stocks">Stocks</option>
                      <option value="options">Options</option>
                    </select>
                  </div>

                  <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-2 text-xs font-semibold text-white/70 ring-1 ring-white/10">
                    <Search className="h-4 w-4 text-white/40" aria-hidden="true" />
                    <input
                      className="w-44 bg-transparent text-white/90 placeholder:text-white/35 outline-none"
                      placeholder="Filter by Symbol"
                      value={symbolFilter}
                      onChange={(e) => setSymbolFilter(e.target.value)}
                    />
                  </div>

                  <div className="flex items-center gap-2 rounded-full bg-white/5 px-3 py-2 text-xs font-semibold text-white/70 ring-1 ring-white/10">
                    <span className="text-white/40">Sort</span>
                    <select
                      className="bg-transparent text-white/90 outline-none"
                      value={sortKey}
                      onChange={(e) => setSortKey(e.target.value as any)}
                      aria-label="Select sort"
                    >
                      <option value="market_value">Market Value</option>
                      <option value="unrealized_pl">Unrealized P/L</option>
                      <option value="day_pl">Day P/L</option>
                      <option value="nav_pct">% of NAV</option>
                    </select>
                  </div>
                </div>

                <div className="text-xs font-semibold text-white/50">
                  {filteredPositions.length} of {positions.length} positions
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="min-w-[1100px] w-full text-left text-sm">
                  <thead className="sticky top-0 z-10 bg-black/30 backdrop-blur-xl">
                    <tr className="border-t border-white/10">
                      <th className="px-5 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Symbol</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Qty</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Avg Entry</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Mark</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Market Value</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Unrealized</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">Day P/L</th>
                      <th className="px-4 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider">% NAV</th>
                      <th className="px-5 py-3 text-xs font-semibold text-white/50 uppercase tracking-wider text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredPositions.length === 0 ? (
                      <tr className="border-t border-white/10">
                        <td className="px-5 py-10 text-white/60" colSpan={9}>
                          No positions. Open{" "}
                          <Link className="text-cyan-300 hover:text-cyan-200 underline" href="/tracking">
                            Tracking
                          </Link>{" "}
                          to start monitoring symbols.
                        </td>
                      </tr>
                    ) : (
                      filteredPositions.map((p) => {
                        const sym = String(p.symbol ?? "—")
                        const qty = toNumber(p.qty)
                        const mv = toNumber(p.market_value)
                        const upl = toNumber(p.unrealized_pl)
                        const dayPl =
                          toNumber(p.unrealized_intraday_pl) ??
                          (() => {
                            const q = toNumber(p.qty)
                            const current = toNumber(p.current_price)
                            const lastday = toNumber(p.lastday_price)
                            if (q !== null && current !== null && lastday !== null) return (current - lastday) * q
                            return 0
                          })()
                        const navPct = nav && nav !== 0 && mv !== null ? mv / nav : null

                        const isOption = isLikelyOption(p)
                        const trackingHref = !isOption && /^[A-Z.]+$/i.test(sym) ? `/tracking/${encodeURIComponent(sym)}` : null

                        return (
                          <tr
                            key={sym}
                            className="border-t border-white/10 transition hover:filter hover:drop-shadow(0_0_18px_rgba(139,92,246,0.22))"
                          >
                            <td className="px-5 py-4">
                              <div className="font-extrabold tracking-tight">{sym}</div>
                              <div className="mt-1 text-xs font-semibold text-white/45">
                                {isOption ? "Option" : "Stock"}
                              </div>
                            </td>
                            <td className={cn("px-4 py-4 font-semibold", qty && qty < 0 ? "text-rose-200" : "text-white/80")}>
                              {qty === null ? "—" : qty.toLocaleString("en-US", { maximumFractionDigits: 4 })}
                            </td>
                            <td className="px-4 py-4 text-white/80">{formatMoney(toNumber(p.avg_entry_price))}</td>
                            <td className="px-4 py-4 text-white/80">{formatMoney(toNumber(p.current_price))}</td>
                            <td className="px-4 py-4 text-white/90">{formatMoney(mv)}</td>
                            <td className={cn("px-4 py-4 font-bold", pnlClass(upl))}>{formatMoney(upl)}</td>
                            <td className={cn("px-4 py-4 font-bold", pnlClass(dayPl))}>{formatMoney(dayPl)}</td>
                            <td className="px-4 py-4 text-white/70">{formatPct(navPct)}</td>
                            <td className="px-5 py-4 text-right">
                              {trackingHref ? (
                                <Link
                                  href={trackingHref}
                                  className="inline-flex items-center justify-center rounded-xl bg-white/5 px-3 py-2 text-xs font-bold text-white/80 ring-1 ring-white/10 transition hover:bg-white/10 hover:ring-white/20 focus:outline-none focus:ring-2 focus:ring-cyan-400/70"
                                >
                                  Open in Tracking
                                </Link>
                              ) : (
                                <span className="text-xs font-semibold text-white/35">—</span>
                              )}
                            </td>
                          </tr>
                        )
                      })
                    )}
                  </tbody>
                  <tfoot>
                    <tr className="border-t border-white/15 bg-black/25">
                      <td className="px-5 py-4 text-xs font-extrabold text-white/70 uppercase tracking-wider">Total</td>
                      <td className="px-4 py-4" />
                      <td className="px-4 py-4" />
                      <td className="px-4 py-4" />
                      <td className="px-4 py-4 font-extrabold text-white/90">{formatMoney(tableTotals.marketValue)}</td>
                      <td className={cn("px-4 py-4 font-extrabold", pnlClass(tableTotals.unrealized))}>{formatMoney(tableTotals.unrealized)}</td>
                      <td className={cn("px-4 py-4 font-extrabold", pnlClass(tableTotals.dayPl))}>{formatMoney(tableTotals.dayPl)}</td>
                      <td className="px-4 py-4 text-white/50">—</td>
                      <td className="px-5 py-4" />
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  )
}
