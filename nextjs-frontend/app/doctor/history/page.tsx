"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { HistoryPanel } from "@/components/history-panel"

export default function DoctorHistory() {
  return (
    <DashboardLayout portal="doctor">
      <HistoryPanel portal="doctor" />
    </DashboardLayout>
  )
}
