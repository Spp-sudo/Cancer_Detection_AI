import type { Metadata } from "next"
import "./globals.css"
import { AuthProvider } from "@/lib/auth-context"
import { ScanHistoryProvider } from "@/lib/scan-history"

export const metadata: Metadata = {
  title: "OncoLens AI",
  description: "Next-generation cancer care intelligence",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0c0414] text-[#e8f4fc] antialiased">
        <AuthProvider>
          <ScanHistoryProvider>
            {children}
          </ScanHistoryProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
