"use client"

import { AnimatePresence, motion } from "framer-motion"
import { X } from "lucide-react"
import { useEffect, useRef, useState } from "react"

import { cn } from "./cn"

export function SettingsDrawer({
  open,
  onClose,
  paperAutoTradeEnabled,
  onRequestEnablePaperAutoTrade,
  onDisablePaperAutoTrade,
  isSaving,
  error,
}: {
  open: boolean
  onClose: () => void
  paperAutoTradeEnabled: boolean
  onRequestEnablePaperAutoTrade: () => void
  onDisablePaperAutoTrade: () => void
  isSaving?: boolean
  error?: string | null
}) {
  const closeButtonRef = useRef<HTMLButtonElement | null>(null)
  const [confirmOpen, setConfirmOpen] = useState(false)

  useEffect(() => {
    if (!open) return
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }
    window.addEventListener("keydown", onKeyDown)
    closeButtonRef.current?.focus()
    return () => window.removeEventListener("keydown", onKeyDown)
  }, [open, onClose])

  useEffect(() => {
    if (!open) setConfirmOpen(false)
  }, [open])

  const onToggle = () => {
    if (isSaving) return
    if (paperAutoTradeEnabled) {
      onDisablePaperAutoTrade()
      return
    }
    setConfirmOpen(true)
  }

  const onConfirmEnable = () => {
    setConfirmOpen(false)
    onRequestEnablePaperAutoTrade()
  }

  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          className="fixed inset-0 z-[100] flex justify-end"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <button
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            aria-label="Close settings"
            onClick={onClose}
          />

          <motion.aside
            className={cn(
              "relative h-full w-full max-w-[420px] border-l border-white/10 bg-black/30 backdrop-blur-xl",
              "shadow-[0_0_50px_rgba(0,0,0,0.7)]",
            )}
            initial={{ x: 24, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 24, opacity: 0 }}
            transition={{ type: "spring", stiffness: 340, damping: 32 }}
            role="dialog"
            aria-modal="true"
            aria-label="Settings"
          >
            <div className="sticky top-0 z-10 flex items-center justify-between border-b border-white/10 bg-black/20 px-5 py-4 backdrop-blur-xl">
              <div className="text-sm font-semibold text-white/90">Settings</div>
              <button
                ref={closeButtonRef}
                type="button"
                className="grid h-9 w-9 place-items-center rounded-xl bg-white/5 ring-1 ring-white/10 transition hover:bg-white/10 hover:ring-white/20 focus:outline-none focus:ring-2 focus:ring-cyan-400/70"
                onClick={onClose}
                aria-label="Close settings"
              >
                <X className="h-4 w-4 text-white/80" aria-hidden="true" />
              </button>
            </div>

            <div className="space-y-4 px-5 py-5">
              <div className="rounded-2xl bg-white/5 p-5 ring-1 ring-white/10 shadow-[0_0_25px_rgba(34,211,238,0.12)]">
                <div className="text-sm font-semibold text-white/90">Trading</div>
                <div className="mt-3 flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-white/90">Enable Alpaca Paper Trading Auto Trading</div>
                    {error ? <div className="mt-2 text-xs text-rose-300">{error}</div> : null}
                  </div>

                  <button
                    type="button"
                    role="switch"
                    aria-checked={paperAutoTradeEnabled}
                    onClick={onToggle}
                    disabled={!!isSaving}
                    className={cn(
                      "relative inline-flex h-7 w-12 flex-none items-center rounded-full ring-1 ring-white/10 transition",
                      paperAutoTradeEnabled ? "bg-[#2DFFB3]/30" : "bg-[#2A2A2A]",
                      isSaving ? "opacity-70" : "hover:ring-white/20",
                      "focus:outline-none focus:ring-2 focus:ring-cyan-400/70",
                    )}
                  >
                    <span
                      className={cn(
                        "inline-block h-5 w-5 translate-x-1 rounded-full bg-white/85 shadow transition",
                        paperAutoTradeEnabled ? "translate-x-6 shadow-[0_0_18px_rgba(45,255,179,0.35)]" : "translate-x-1",
                      )}
                    />
                  </button>
                </div>
              </div>
            </div>

            <AnimatePresence>
              {confirmOpen ? (
                <motion.div
                  className="absolute inset-0 z-20 grid place-items-center bg-black/60 px-5"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <motion.div
                    className="w-full max-w-sm rounded-2xl bg-black/40 p-5 ring-1 ring-white/10 backdrop-blur-xl"
                    initial={{ y: 8, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    exit={{ y: 8, opacity: 0 }}
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  >
                    <div className="text-sm font-semibold text-white/90">Confirm Enable</div>
                    <div className="mt-2 text-xs leading-relaxed text-white/60">
                      This will automatically submit paper trading orders.
                    </div>
                    <div className="mt-4 flex items-center justify-end gap-2">
                      <button
                        type="button"
                        className="rounded-xl bg-white/5 px-4 py-2 text-xs font-semibold text-white/80 ring-1 ring-white/10 transition hover:bg-white/10 hover:ring-white/20 focus:outline-none focus:ring-2 focus:ring-cyan-400/70"
                        onClick={() => setConfirmOpen(false)}
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        className="rounded-xl bg-emerald-400/15 px-4 py-2 text-xs font-semibold text-emerald-200 ring-1 ring-emerald-400/25 transition hover:bg-emerald-400/20 focus:outline-none focus:ring-2 focus:ring-emerald-300/60"
                        onClick={onConfirmEnable}
                      >
                        Enable
                      </button>
                    </div>
                  </motion.div>
                </motion.div>
              ) : null}
            </AnimatePresence>
          </motion.aside>
        </motion.div>
      ) : null}
    </AnimatePresence>
  )
}
