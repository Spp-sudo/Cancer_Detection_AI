"use client"

import { useRouter, usePathname } from "next/navigation"
import { useAuth } from "@/lib/auth-context"
import { MeshBackground } from "@/components/ui/glass-card"
import { cn } from "@/lib/utils"

interface NavItem { label: string; icon: string; href: string }

const USER_NAV: NavItem[] = [
  { label: "Upload Scan",  icon: "📤", href: "/user/dashboard" },
  { label: "My Results",   icon: "📊", href: "/user/history" },
  { label: "Profile",      icon: "👤", href: "/user/profile" },
]

const DOCTOR_NAV: NavItem[] = [
  { label: "Upload Study",    icon: "📤", href: "/doctor/dashboard" },
  { label: "Review Scans",    icon: "🔬", href: "/doctor/review" },
  { label: "Patient Records", icon: "📋", href: "/doctor/history" },
  { label: "System",          icon: "⚙️", href: "/doctor/system" },
  { label: "Profile",         icon: "👤", href: "/doctor/profile" },
]

export function DashboardLayout({ children, portal }: { children: React.ReactNode; portal: "user" | "doctor" }) {
  const router = useRouter()
  const pathname = usePathname()
  const { email, logout } = useAuth()
  const accent = portal === "user" ? "#4dffc9" : "#5eb3ff"
  const nav = portal === "user" ? USER_NAV : DOCTOR_NAV

  return (
    <div className="relative flex min-h-screen">
      <MeshBackground />

      {/* Sidebar */}
      <aside className="relative z-10 flex w-56 flex-shrink-0 flex-col border-r border-[rgba(120,200,255,0.12)] bg-[rgba(6,14,28,0.85)] backdrop-blur-xl p-4">
        <div className="mb-6 flex items-center gap-2">
          <span className="text-xl">◈</span>
          <span className="font-bold text-sm">
            OncoLens <span style={{ color: accent }}>{portal === "user" ? "Patient" : "Clinical"}</span>
          </span>
        </div>

        <nav className="flex flex-col gap-1 flex-1">
          {nav.map(item => (
            <button
              key={item.href}
              onClick={() => router.push(item.href)}
              className={cn(
                "flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-sm text-left transition-colors",
                pathname === item.href
                  ? "bg-white/10 font-semibold text-white"
                  : "text-[#7a9bb8] hover:bg-white/5 hover:text-white"
              )}
            >
              <span>{item.icon}</span>{item.label}
            </button>
          ))}
        </nav>

        <div className="border-t border-white/[0.06] pt-3 mt-3 flex flex-col gap-1">
          {email && <p className="text-xs text-[#7a9bb8] mb-1 truncate px-1">{email}</p>}
          <button onClick={() => { logout(); router.push("/") }}
            className="w-full rounded-xl border border-white/10 px-3 py-2 text-xs text-[#7a9bb8] hover:text-white hover:border-white/20 transition-colors text-left">
            Sign out
          </button>
          <button onClick={() => router.push("/")}
            className="w-full rounded-xl px-3 py-2 text-xs text-[#7a9bb8] hover:text-white transition-colors text-left">
            ⇄ Switch portal
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="relative z-10 flex-1 overflow-auto p-6 animate-fade-in">
        {children}
      </main>
    </div>
  )
}
