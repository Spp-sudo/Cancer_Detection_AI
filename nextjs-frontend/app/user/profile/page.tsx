"use client"

import { useAuth } from "@/lib/auth-context"
import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard, Eyebrow, PageTitle } from "@/components/ui/glass-card"

export default function UserProfile() {
  const { email } = useAuth()
  const name = email?.split("@")[0] ?? "User"

  return (
    <DashboardLayout portal="user">
      <div className="max-w-lg">
        <Eyebrow accent="#4dffc9">Account</Eyebrow>
        <PageTitle accent="#4dffc9">Your Profile</PageTitle>
        <GlassCard className="text-center py-8">
          <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full text-3xl font-bold"
            style={{ background: "linear-gradient(135deg,#4dffc9,#0c0414)" }}>
            {name[0].toUpperCase()}
          </div>
          <h3 className="text-xl font-bold capitalize">{name}</h3>
          <p className="text-[#7a9bb8] text-sm mt-1">{email}</p>
          <div className="mt-6 flex justify-center gap-8 border-t border-white/[0.06] pt-6">
            {[["Studies","—"],["Role","Patient"],["Since","2025"]].map(([label, val]) => (
              <div key={label}>
                <p className="text-xs text-[#7a9bb8] uppercase">{label}</p>
                <p className="font-bold mt-1" style={{ color: label === "Role" ? "#4dffc9" : "white" }}>{val}</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  )
}
