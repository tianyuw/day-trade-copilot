import Link from "next/link"

export function NavigationBar() {
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
          
        </nav>
      </div>
    </header>
  )
}

