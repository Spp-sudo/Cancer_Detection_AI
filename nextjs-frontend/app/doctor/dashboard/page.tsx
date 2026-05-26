"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { AnalysisPanel } from "@/components/analysis-panel"

export default function DoctorDashboard() {
  return (
    <DashboardLayout portal="doctor">
      <AnalysisPanel portal="doctor" />
    </DashboardLayout>
  )
}
