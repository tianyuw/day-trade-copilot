import Link from "next/link"

export function NavigationBar() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-black/20 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="inline-flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-white/8 ring-1 ring-white/10">
            <svg className="h-5 w-5 text-amber-300" aria-hidden="true">
              <use href="#icon-bolt" />
            </svg>
          </div>
          <div className="min-w-0">
            <div className="truncate text-sm font-extrabold tracking-tight">0DTE Copilot</div>
          </div>
        </Link>

        <nav className="flex items-center gap-2 text-sm">
          <Link
            href="/dashboard"
            className="rounded-2xl bg-white/6 px-4 py-2 font-semibold text-white/80 ring-1 ring-white/10 hover:bg-white/8"
          >
            Dashboard
          </Link>
        </nav>
      </div>
    </header>
  )
}

