import Image from "next/image"

import { NeonButton } from "../components/NeonButton"

export default function Home() {
  return (
    <main className="min-h-screen bg-neon-radial">
      <div className="mx-auto max-w-6xl px-6 py-14">
        <div className="flex flex-col gap-10">
          <div className="flex items-start justify-between gap-8">
            <div className="max-w-2xl">
              <div className="inline-flex items-center gap-2 rounded-full bg-white/8 px-4 py-2 text-xs font-semibold ring-1 ring-white/10 backdrop-blur-md">
                <svg className="h-4 w-4 text-amber-300" aria-hidden="true">
                  <use href="#icon-bolt" />
                </svg>
                <span className="text-white/80">Quant filter → AI verify → instant action plan</span>
              </div>

              <h1 className="mt-6 text-4xl font-black tracking-tight sm:text-6xl">
                Trade the minute.
                <span className="block bg-gradient-to-r from-cyan-300 via-violet-400 to-amber-300 bg-clip-text text-transparent">
                  0DTE Copilot.
                </span>
              </h1>

              <p className="mt-5 text-base leading-relaxed text-white/70 sm:text-lg">
                Real-time 1m K线监控 + 回放复盘，一眼看清突破点位与节奏。Gen-Z 风格但不花里胡哨：快、狠、准。
              </p>

              <div className="mt-7 flex flex-wrap items-center gap-3">
                <NeonButton href="/dashboard">Enter Dashboard</NeonButton>
                <a
                  href="/ui-previews/index.html"
                  className="rounded-2xl bg-white/6 px-5 py-3 text-sm font-semibold text-white/80 ring-1 ring-white/10 backdrop-blur-md hover:bg-white/8"
                >
                  UI Previews
                </a>
              </div>

              <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
                {[
                  { k: "Playback", v: "复盘回放" },
                  { k: "Realtime", v: "实时推送" },
                  { k: "Grid", v: "网格监控" },
                  { k: "Neon", v: "霓虹氛围" },
                ].map((x) => (
                  <div
                    key={x.k}
                    className="rounded-3xl bg-white/6 p-4 text-sm shadow-neo ring-1 ring-white/10 backdrop-blur-md"
                  >
                    <div className="text-[11px] font-bold text-white/60">{x.k}</div>
                    <div className="mt-2 font-extrabold">{x.v}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative hidden w-[320px] flex-none sm:block">
              <div className="absolute -inset-4 rounded-[44px] bg-gradient-to-b from-cyan-300/20 via-violet-500/15 to-amber-300/10 blur-2xl" />
              <div className="relative overflow-hidden rounded-[44px] bg-white/6 p-3 shadow-glass ring-1 ring-white/10 backdrop-blur-xl">
                <div className="overflow-hidden rounded-[36px] bg-black/50">
                  <Image
                    src="https://images.unsplash.com/photo-1640826511780-7a1b0f66e4ae?auto=format&fit=crop&w=800&q=80"
                    alt="Placeholder"
                    width={800}
                    height={1200}
                    className="h-[560px] w-full object-cover opacity-80"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-3xl bg-white/5 p-6 ring-1 ring-white/10 backdrop-blur-md">
            <div className="flex items-center justify-between gap-4">
              <div className="text-sm font-semibold text-white/70">
                Built for replay-first development: 先复盘，再上实盘。
              </div>
              <div className="text-xs text-white/50">Alpaca Data API + OpenRouter Gemini</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

