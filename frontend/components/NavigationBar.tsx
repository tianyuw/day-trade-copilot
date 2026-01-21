"use client"

import Link from "next/link"
import { Settings as SettingsIcon } from "lucide-react"
import { useCallback, useEffect, useMemo, useState } from "react"

import { SettingsDrawer } from "./SettingsDrawer"

export function NavigationBar() {
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [paperAutoTradeEnabled, setPaperAutoTradeEnabled] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const baseHttp = useMemo(() => {
    if (typeof window === "undefined") return ""
    return process.env.NEXT_PUBLIC_BACKEND_API ?? `http://${window.location.hostname}:${process.env.NEXT_PUBLIC_BACKEND_API_PORT ?? "8000"}`
  }, [])

  useEffect(() => {
    if (typeof window === "undefined") return
    const raw = window.localStorage.getItem("paperAutoTradeEnabled")
    if (raw === "true") setPaperAutoTradeEnabled(true)
    if (raw === "false") setPaperAutoTradeEnabled(false)
  }, [])

  useEffect(() => {
    if (!baseHttp) return
    const run = async () => {
      try {
        const res = await fetch(`${baseHttp}/api/settings/trading`, { method: "GET" })
        if (!res.ok) return
        const body = (await res.json()) as { paper_auto_trade_enabled?: unknown }
        if (typeof body.paper_auto_trade_enabled !== "boolean") return
        setPaperAutoTradeEnabled(body.paper_auto_trade_enabled)
        window.localStorage.setItem("paperAutoTradeEnabled", String(body.paper_auto_trade_enabled))
      } catch {
      }
    }
    run()
  }, [baseHttp])

  const updatePaperAutoTradeEnabled = useCallback(
    async (nextValue: boolean) => {
      if (!baseHttp) return
      setIsSaving(true)
      setError(null)
      const previous = paperAutoTradeEnabled
      setPaperAutoTradeEnabled(nextValue)
      try {
        window.localStorage.setItem("paperAutoTradeEnabled", String(nextValue))
        const res = await fetch(`${baseHttp}/api/settings/trading`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ paper_auto_trade_enabled: nextValue }),
        })
        if (!res.ok) {
          throw new Error("save_failed")
        }
      } catch {
        setPaperAutoTradeEnabled(previous)
        window.localStorage.setItem("paperAutoTradeEnabled", String(previous))
        setError("Failed to save settings. Please try again.")
      } finally {
        setIsSaving(false)
      }
    },
    [baseHttp, paperAutoTradeEnabled],
  )

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-black/20 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="inline-flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-tr from-cyan-500/20 to-purple-500/20 ring-1 ring-white/10 shadow-[0_0_15px_rgba(34,211,238,0.2)]">
            <svg className="h-5 w-5 text-cyan-300" aria-hidden="true">
              <use href="#icon-trend" />
            </svg>
          </div>
          <div className="min-w-0">
            <div className="truncate text-sm font-extrabold tracking-tight bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">Day Trade Copilot</div>
          </div>
        </Link>

        <nav className="flex items-center gap-2 text-sm">
          <button
            type="button"
            className="grid h-10 w-10 place-items-center rounded-2xl bg-white/5 ring-1 ring-white/10 transition hover:bg-white/10 hover:ring-white/20 focus:outline-none focus:ring-2 focus:ring-cyan-400/70"
            onClick={() => setDrawerOpen(true)}
            aria-label="Open settings"
          >
            <SettingsIcon className="h-5 w-5 text-white/70" aria-hidden="true" />
          </button>
        </nav>
      </div>
      <SettingsDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        paperAutoTradeEnabled={paperAutoTradeEnabled}
        onRequestEnablePaperAutoTrade={() => updatePaperAutoTradeEnabled(true)}
        onDisablePaperAutoTrade={() => updatePaperAutoTradeEnabled(false)}
        isSaving={isSaving}
        error={error}
      />
    </header>
  )
}
