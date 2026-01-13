import "./globals.css"

import { NavigationBar } from "../components/NavigationBar"

export const metadata = {
  title: "0DTE Copilot",
  description: "Quant filter + AI verify, built for fast 0DTE decisions.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <svg width="0" height="0" style={{ position: "absolute" }} aria-hidden="true" focusable="false">
          <symbol id="icon-bolt" viewBox="0 0 24 24">
            <path
              d="M13 2L3 14h7l-1 8 12-14h-7l-1-6z"
              fill="currentColor"
            />
          </symbol>
          <symbol id="icon-fire" viewBox="0 0 24 24">
            <path
              d="M12 22c4.4 0 8-3.4 8-7.7 0-3.6-2.4-5.7-4.2-7.3-.9-.8-1.6-1.5-2-2.2-.3.9-.8 1.7-1.5 2.4-.9.9-2 1.8-2 3.2 0 1.6 1.3 2.7 2.8 2.7 1.6 0 2.9-1.2 2.9-2.8 1.8 1.4 3 3.1 3 5.1 0 3.3-2.8 6-6.2 6-3.5 0-6.3-2.7-6.3-6 0-4.3 3.3-6.4 4.8-9.9.6 1.8 1.9 3 3.3 4.2 1.9 1.7 3.9 3.4 3.9 6.6 0 4.3-3.6 7.7-8 7.7z"
              fill="currentColor"
            />
          </symbol>
          <symbol id="icon-spark" viewBox="0 0 24 24">
            <path
              d="M3 14l4-4 4 4 6-8 4 4"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </symbol>
        </svg>
        <NavigationBar />
        {children}
      </body>
    </html>
  )
}
