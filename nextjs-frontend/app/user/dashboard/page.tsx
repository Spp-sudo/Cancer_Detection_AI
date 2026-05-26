"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { AnalysisPanel } from "@/components/analysis-panel"

export default function UserDashboard() {
  return (
    <DashboardLayout portal="user">
      <AnalysisPanel portal="user" />
    </DashboardLayout>
  )
}
