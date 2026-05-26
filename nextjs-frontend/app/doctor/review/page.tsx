"use client"

import { useState } from "react"
import { ClipboardList, ChevronDown, ChevronUp, Download, Save } from "lucide-react"
import { useScanHistory, type ScanRecord } from "@/lib/scan-history"
import { generateReport } from "@/lib/report"
import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard, Eyebrow, PageTitle } from "@/components/ui/glass-card"

function ReviewCard({ scan }: { scan: ScanRecord }) {
  const { addDoctorNote } = useScanHistory()
  const [open, setOpen] = useState(false)
  const [note, setNote] = useState(scan.doctor_note ?? "")
  const [saved, setSaved] = useState(false)
  const cm = scan.confidence_metrics

  const save = () => {
    addDoctorNote(scan.study_id, note)
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  const download = () => {
    const text = generateReport(scan, scan.filename, "", note, "doctor")
    const blob = new Blob([text], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url; a.download = `review_${scan.study_id}.txt`; a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <GlassCard className="p-0 overflow-hidden">
      {/* Header */}
      <button className="w-full flex items-center gap-3 px-4 py-4 hover:bg-white/[0.03] transition-colors text-left"
        onClick={() => setOpen(o => !o)}>
        <span className={`flex-shrink-0 rounded-full px-2.5 py-0.5 text-xs font-semibold ${scan.classification === "Malignant" ? "bg-red-500/20 text-red-300" : "bg-green-500/20 text-green-300"}`}>
          {scan.classification}
        </span>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold truncate">{scan.filename}</p>
          <p className="text-xs text-[#7a9bb8]">{scan.model_name} · {new Date(scan.created_at).toLocaleString()}</p>
        </div>
        <div className="text-right hidden sm:block">
          <p className="text-xs text-[#7a9bb8]">Confidence</p>
          <p className="text-sm font-bold text-[#5eb3ff]">{(cm.primary_confidence * 100).toFixed(0)}%</p>
        </div>
        <span className="font-mono text-xs text-[#7a9bb8]">{scan.study_id}</span>
        {scan.doctor_note && <span title="Has physician note" className="text-[#5eb3ff] text-xs">📝</span>}
        {open ? <ChevronUp size={14} className="text-[#7a9bb8] flex-shrink-0" /> : <ChevronDown size={14} className="text-[#7a9bb8] flex-shrink-0" />}
      </button>

      {open && (
        <div className="border-t border-white/[0.06] px-4 py-4 flex flex-col gap-4">
          {/* Metrics */}
          <div className="grid grid-cols-3 gap-3">
            {[
              ["Confidence",  `${(cm.primary_confidence * 100).toFixed(1)}%`],
              ["Benign",      `${(cm.benign_probability * 100).toFixed(1)}%`],
              ["Malignant",   `${(cm.malignancy_probability * 100).toFixed(1)}%`],
            ].map(([label, val]) => (
              <div key={label} className="rounded-xl border border-white/[0.06] bg-black/20 p-3 text-center">
                <p className="text-xs text-[#7a9bb8]">{label}</p>
                <p className="text-base font-bold text-[#5eb3ff] mt-0.5">{val}</p>
              </div>
            ))}
          </div>

          {/* Predictions */}
          {scan.predictions && scan.predictions.length > 0 && (
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-[#5eb3ff] mb-2">AI Predictions</p>
              <div className="flex flex-col gap-1.5">
                {scan.predictions.slice(0, 5).map(p => (
                  <div key={p.label} className="flex items-center gap-3">
                    <span className="w-40 text-xs text-[#7a9bb8] truncate">{p.label.replace(/_/g, " ")}</span>
                    <div className="flex-1 h-1.5 rounded-full bg-white/10 overflow-hidden">
                      <div className="h-full rounded-full bg-[#5eb3ff]" style={{ width: `${p.probability * 100}%` }} />
                    </div>
                    <span className="text-xs w-10 text-right">{(p.probability * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* AI recommendation */}
          <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] px-3 py-2">
            <p className="text-xs font-semibold text-[#5eb3ff] mb-1">AI Recommendation</p>
            <p className="text-xs text-[#7a9bb8] leading-relaxed">{scan.recommendation}</p>
          </div>

          {/* Doctor note */}
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-[#5eb3ff] mb-2">Physician Review Notes</p>
            <textarea
              className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2.5 text-sm outline-none focus:border-[#5eb3ff] resize-none transition-colors"
              rows={4}
              placeholder="Add your clinical observations, diagnosis confirmation, treatment plan, or follow-up instructions…"
              value={note}
              onChange={e => setNote(e.target.value)}
            />
            <div className="flex gap-2 mt-2">
              <button onClick={save}
                className="flex items-center gap-1.5 rounded-lg border border-[rgba(94,179,255,0.3)] bg-[rgba(94,179,255,0.1)] px-3 py-1.5 text-xs text-[#5eb3ff] hover:bg-[rgba(94,179,255,0.2)] transition-colors">
                <Save size={12} /> {saved ? "Saved ✓" : "Save Note"}
              </button>
              <button onClick={download}
                className="flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs hover:bg-white/10 transition-colors">
                <Download size={12} /> Download Report
              </button>
            </div>
          </div>
        </div>
      )}
    </GlassCard>
  )
}

export default function DoctorReview() {
  const { scans } = useScanHistory()

  return (
    <DashboardLayout portal="doctor">
      <div className="flex flex-col gap-5 max-w-4xl">
        <div>
          <Eyebrow accent="#5eb3ff">Clinical Review</Eyebrow>
          <PageTitle accent="#5eb3ff">Doctor Review Dashboard</PageTitle>
          <p className="text-[#7a9bb8] text-sm">Review AI-analyzed scans, add physician notes, and generate professional reports.</p>
        </div>

        {/* Summary stats */}
        {scans.length > 0 && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              ["Pending Review", scans.filter(s => !s.doctor_note).length],
              ["Reviewed",       scans.filter(s => s.doctor_note).length],
              ["Malignant",      scans.filter(s => s.classification === "Malignant").length],
              ["Total Scans",    scans.length],
            ].map(([label, val]) => (
              <GlassCard key={label as string} className="text-center p-3">
                <p className="text-xs text-[#7a9bb8] uppercase tracking-widest">{label}</p>
                <p className="text-xl font-bold mt-1 text-[#5eb3ff]">{val}</p>
              </GlassCard>
            ))}
          </div>
        )}

        {scans.length === 0 ? (
          <GlassCard className="text-center py-16 animate-float">
            <ClipboardList size={48} className="mx-auto mb-4 text-[#7a9bb8]" />
            <p className="font-semibold text-lg">No scans to review</p>
            <p className="text-[#7a9bb8] text-sm mt-2">Run a diagnostic analysis first — scans will appear here for physician review.</p>
          </GlassCard>
        ) : (
          <div className="flex flex-col gap-3">
            {scans.map(scan => <ReviewCard key={scan.study_id} scan={scan} />)}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
