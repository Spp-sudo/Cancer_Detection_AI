"use client"

import { createContext, useContext, useState, ReactNode } from "react"
import type { PredictResult } from "./api"

export interface ScanRecord extends PredictResult {
  filename: string
  model_name: string
  created_at: string
  doctor_note?: string
}

interface ScanHistoryCtx {
  scans: ScanRecord[]
  addScan: (s: ScanRecord) => void
  addDoctorNote: (study_id: string, note: string) => void
}

const Ctx = createContext<ScanHistoryCtx | null>(null)

export function ScanHistoryProvider({ children }: { children: ReactNode }) {
  const [scans, setScans] = useState<ScanRecord[]>([])

  const addScan = (s: ScanRecord) =>
    setScans(prev => [s, ...prev.filter(x => x.study_id !== s.study_id)])

  const addDoctorNote = (study_id: string, note: string) =>
    setScans(prev => prev.map(s => s.study_id === study_id ? { ...s, doctor_note: note } : s))

  return <Ctx.Provider value={{ scans, addScan, addDoctorNote }}>{children}</Ctx.Provider>
}

export function useScanHistory() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error("useScanHistory must be inside ScanHistoryProvider")
  return ctx
}
