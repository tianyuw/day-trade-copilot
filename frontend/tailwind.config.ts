import type { Config } from "tailwindcss"

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#05050a",
          900: "#0b0b14",
          800: "#111125",
        },
      },
      boxShadow: {
        neo: "inset 8px 8px 18px rgba(0,0,0,.55), inset -8px -8px 18px rgba(255,255,255,.06)",
        neoHover: "inset 10px 10px 22px rgba(0,0,0,.55), inset -10px -10px 22px rgba(255,255,255,.08)",
        glass: "0 0 0 1px rgba(255,255,255,.08), 0 20px 60px rgba(0,0,0,.55)",
      },
      backgroundImage: {
        "neon-radial":
          "radial-gradient(1200px circle at 20% 10%, rgba(124,58,237,.35), transparent 55%), radial-gradient(900px circle at 80% 30%, rgba(34,211,238,.25), transparent 45%), radial-gradient(900px circle at 50% 90%, rgba(251,191,36,.18), transparent 40%)",
      },
      keyframes: {
        glow: {
          "0%, 100%": { filter: "drop-shadow(0 0 0 rgba(34,211,238,.0))" },
          "50%": { filter: "drop-shadow(0 0 18px rgba(34,211,238,.45))" },
        },
        dash: {
          "0%": { strokeDashoffset: "240" },
          "100%": { strokeDashoffset: "0" },
        },
        "gradient-x": {
          "0%, 100%": {
            "background-size": "200% 200%",
            "background-position": "left center",
          },
          "50%": {
            "background-size": "200% 200%",
            "background-position": "right center",
          },
        },
      },
      animation: {
        glow: "glow 2.8s ease-in-out infinite",
        dash: "dash 1.6s ease-out forwards",
        "gradient-x": "gradient-x 15s ease infinite",
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
    },
  },
  plugins: [],
} satisfies Config

