"use client"

import { motion } from "framer-motion"
import Link from "next/link"

import { cn } from "./cn"

export function NeonButton({
  href,
  children,
  className,
}: {
  href: string
  children: React.ReactNode
  className?: string
}) {
  return (
    <motion.div whileHover={{ y: -1 }} whileTap={{ scale: 0.98 }}>
      <Link
        href={href}
        className={cn(
          "relative inline-flex items-center justify-center gap-2 rounded-2xl px-5 py-3 text-sm font-semibold",
          "bg-white/10 shadow-glass backdrop-blur-md",
          "ring-1 ring-white/10 hover:ring-white/20",
          "transition",
          className,
        )}
      >
        <span className="absolute -inset-1 rounded-[18px] bg-gradient-to-r from-cyan-400/25 via-violet-500/25 to-amber-300/20 blur-xl" />
        <span className="relative">{children}</span>
      </Link>
    </motion.div>
  )
}

