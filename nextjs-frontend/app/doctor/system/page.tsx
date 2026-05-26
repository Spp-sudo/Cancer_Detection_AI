"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/lib/auth-context"
import { api } from "@/lib/api"
import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard, Eyebrow, PageTitle, MetricGrid } from "@/components/ui/glass-card"

export default function DoctorSystem() {
  const { token } = useAuth()
  const [health, setHealth] = useState<any>(null)
  const [error, setError] = useState("")

  useEffect(() => {
    api.health(token ?? undefined).then(setHealth).catch(e => setError(e.message))
  }, [token])

  return (
    <DashboardLayout portal="doctor">
      <div className="max-w-2xl">
        <Eyebrow accent="#5eb3ff">Infrastructure</Eyebrow>
        <PageTitle accent="#5eb3ff">System Status</PageTitle>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        {health && (
          <>
            <MetricGrid items={[
              ["Status",  health.status ?? "—"],
              ["Version", health.version ?? "—"],
              ["Model",   (health.model_name ?? "—").slice(0, 10)],
              ["DB",      health.database ?? "—"],
            ]} />
            <GlassCard>
              <p className="text-sm font-semibold mb-2">Model loaded</p>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold ${health.model_loaded ? "bg-green-500/20 text-green-300" : "bg-red-500/20 text-red-300"}`}>
                {health.model_loaded ? "✓ Ready" : "✗ Not loaded"}
              </span>
            </GlassCard>
          </>
        )}
      </div>
    </DashboardLayout>
  )
}
