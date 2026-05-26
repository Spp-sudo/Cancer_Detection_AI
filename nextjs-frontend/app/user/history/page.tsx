"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { HistoryPanel } from "@/components/history-panel"

export default function UserHistory() {
  return (
    <DashboardLayout portal="user">
      <HistoryPanel portal="user" />
    </DashboardLayout>
  )
}
