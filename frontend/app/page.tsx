import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen bg-neon-radial text-white font-sans selection:bg-cyan-500/30">
      
      <div className="mx-auto max-w-7xl px-6 py-14 lg:py-24">
        <div className="flex flex-col gap-16 lg:flex-row lg:items-center">
          
          {/* Left Content */}
          <div className="flex-1 max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/5 px-4 py-1.5 text-xs font-semibold ring-1 ring-white/10 backdrop-blur-md mb-8">
              <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-white/80 tracking-wide uppercase">v1.3 Available Now</span>
            </div>

            <h1 className="text-5xl font-black tracking-tight sm:text-7xl leading-[1.1]">
              Master the <br />
              <span className="bg-gradient-to-r from-cyan-300 via-violet-400 to-amber-300 bg-clip-text text-transparent animate-gradient-x">
                Market Pulse
              </span>
              <br /> with AI.
            </h1>

            <p className="mt-6 text-lg leading-relaxed text-white/60 max-w-lg">
              Real-time 1m K-line monitoring + Replay Console. 
              <br/>
              Capture 0DTE opportunities with Gen-Z speed and AI precision.
            </p>

            <div className="mt-10 flex flex-wrap items-center gap-4">
              <Link href="/dashboard">
                <div className="group relative px-8 py-4 bg-white text-black font-bold rounded-2xl shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:shadow-[0_0_35px_rgba(255,255,255,0.45)] transition-all duration-300 transform hover:-translate-y-0.5 overflow-hidden cursor-pointer">
                  <span className="relative z-10 flex items-center gap-2">
                    Enter Replay Console
                    <svg className="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-200 via-white to-purple-200 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
              </Link>
              
              <Link href="/ui-previews/index.html" className="px-6 py-4 rounded-2xl bg-white/5 text-white/70 font-semibold ring-1 ring-white/10 hover:bg-white/10 transition-colors">
                View Design System
              </Link>
            </div>

            <div className="mt-16 grid grid-cols-2 gap-4 sm:grid-cols-4 border-t border-white/10 pt-8">
              {[
                { label: "Latency", val: "<50ms" },
                { label: "AI Model", val: "Gemini 3 Pro" },
                { label: "Coverage", val: "US Stocks" },
                { label: "Style", val: "Dark Gen-Z" },
              ].map((stat) => (
                <div key={stat.label}>
                  <div className="text-xs font-medium text-white/40 uppercase tracking-wider">{stat.label}</div>
                  <div className="mt-1 text-xl font-bold text-white/90">{stat.val}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Visual */}
          <div className="flex-1 relative hidden lg:block">
            <div className="absolute -inset-10 bg-gradient-to-tr from-cyan-500/20 via-purple-500/20 to-amber-500/20 blur-3xl rounded-full opacity-60 animate-pulse-slow" />
            
            <div className="relative rounded-[2rem] border border-white/10 bg-black/40 backdrop-blur-xl shadow-2xl overflow-hidden transform rotate-[-2deg] hover:rotate-0 transition-transform duration-700 ease-out">
              <div className="absolute inset-0 bg-grid-white/[0.05] [mask-image:linear-gradient(0deg,transparent,black)]" />
              
              {/* Mock Interface */}
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500/50" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                    <div className="w-3 h-3 rounded-full bg-green-500/50" />
                  </div>
                  <div className="h-2 w-20 rounded-full bg-white/10" />
                </div>
                
                <div className="space-y-4">
                  <div className="flex gap-4">
                    <div className="w-2/3 h-48 rounded-xl bg-gradient-to-b from-white/5 to-transparent ring-1 ring-white/10 relative overflow-hidden">
                       {/* Mock Chart Line */}
                       <svg className="absolute bottom-0 left-0 right-0 h-full w-full text-cyan-400 opacity-50" preserveAspectRatio="none">
                         <path d="M0 100 Q 50 50 100 80 T 200 40 T 300 90 T 400 20 L 400 150 L 0 150 Z" fill="url(#gradient)" />
                         <path d="M0 100 Q 50 50 100 80 T 200 40 T 300 90 T 400 20" stroke="currentColor" strokeWidth="2" fill="none" />
                         <defs>
                           <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
                             <stop offset="0%" stopColor="currentColor" stopOpacity="0.3" />
                             <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
                           </linearGradient>
                         </defs>
                       </svg>
                    </div>
                    <div className="w-1/3 space-y-3">
                      <div className="h-12 rounded-lg bg-white/5 ring-1 ring-white/10" />
                      <div className="h-12 rounded-lg bg-white/5 ring-1 ring-white/10" />
                      <div className="h-20 rounded-lg bg-indigo-500/20 ring-1 ring-indigo-500/50 flex items-center justify-center">
                        <span className="text-indigo-300 font-bold">AI Analysis</span>
                      </div>
                    </div>
                  </div>
                  <div className="h-8 w-1/2 rounded-lg bg-white/5 ring-1 ring-white/10" />
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  )
}
