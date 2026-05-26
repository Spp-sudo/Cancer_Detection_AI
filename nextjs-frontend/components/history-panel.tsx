"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp, Download, FileText } from "lucide-react"
import { useScanHistory, type ScanRecord } from "@/lib/scan-history"
import { generateReport } from "@/lib/report"
import { GlassCard, Eyebrow, PageTitle } from "@/components/ui/glass-card"

function downloadTxt(scan: ScanRecord, portal: "user" | "doctor") {
  const text = generateReport(scan, scan.filename, "", scan.doctor_note ?? "", portal)
  const blob = new Blob([text], { type: "text/plain" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `oncolens_report_${scan.study_id}.txt`
  a.click()
  URL.revokeObjectURL(url)
}

function ExpandedRow({ scan, portal }: { scan: ScanRecord; portal: "user" | "doctor" }) {
  const accent = portal === "user" ? "#4dffc9" : "#5eb3ff"
  const cm = scan.confidence_metrics

  return (
    <div className="border-t border-white/[0.06] px-4 py-4 bg-white/[0.02]">
      <div className="grid gap-4 md:grid-cols-2">
        {/* Metrics */}
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest mb-2" style={{ color: accent }}>Confidence Metrics</p>
          <div className="flex flex-col gap-2">
            {[
              ["Primary confidence", cm.primary_confidence],
              ["Benign probability", cm.benign_probability],
              ["Malignant probability", cm.malignancy_probability],
            ].map(([label, val]) => (
              <div key={label as string} className="flex items-center gap-3">
                <span className="w-40 text-xs text-[#7a9bb8]">{label}</span>
                <div className="flex-1 h-1.5 rounded-full bg-white/10 overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${(val as number) * 100}%`, background: accent }} />
                </div>
                <span className="text-xs w-10 text-right">{((val as number) * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top predictions */}
        {scan.predictions && scan.predictions.length > 0 && (
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest mb-2" style={{ color: accent }}>Top Predictions</p>
            <div className="flex flex-col gap-1.5">
              {scan.predictions.slice(0, 5).map(p => (
                <div key={p.label} className="flex items-center gap-2">
                  <span className="w-36 text-xs text-[#7a9bb8] truncate">{p.label.replace(/_/g, " ")}</span>
                  <div className="flex-1 h-1 rounded-full bg-white/10 overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${p.probability * 100}%`, background: accent }} />
                  </div>
                  <span className="text-xs w-8 text-right">{(p.probability * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Recommendation */}
      <div className="mt-4">
        <p className="text-xs font-semibold uppercase tracking-widest mb-1" style={{ color: accent }}>Recommendation</p>
        <p className="text-xs text-[#7a9bb8] leading-relaxed">{scan.recommendation}</p>
      </div>

      {scan.doctor_note && (
        <div className="mt-3 rounded-xl border border-[rgba(94,179,255,0.2)] bg-[rgba(94,179,255,0.05)] px-3 py-2">
          <p className="text-xs font-semibold text-[#5eb3ff] mb-1">Physician Note</p>
          <p className="text-xs text-[#7a9bb8]">{scan.doctor_note}</p>
        </div>
      )}

      <div className="mt-4 flex gap-2">
        <button
          onClick={() => downloadTxt(scan, portal)}
          className="flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs hover:bg-white/10 transition-colors"
        >
          <Download size={12} /> Download Report
        </button>
      </div>
    </div>
  )
}

export function HistoryPanel({ portal }: { portal: "user" | "doctor" }) {
  const { scans } = useScanHistory()
  const accent = portal === "user" ? "#4dffc9" : "#5eb3ff"
  const [expanded, setExpanded] = useState<string | null>(null)

  const toggle = (id: string) => setExpanded(e => e === id ? null : id)

  return (
    <div className="flex flex-col gap-4 max-w-4xl">
      <div>
        <Eyebrow accent={accent}>{portal === "user" ? "Your history" : "Records"}</Eyebrow>
        <PageTitle accent={accent}>{portal === "user" ? "My Health Timeline" : "Patient Records & Analytics"}</PageTitle>
      </div>

      {/* Stats row for doctor */}
      {portal === "doctor" && scans.length > 0 && (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {[
            ["Total Studies", scans.length],
            ["Malignant", scans.filter(r => r.classification === "Malignant").length],
            ["Benign", scans.filter(r => r.classification === "Benign").length],
            ["With Notes", scans.filter(r => r.doctor_note).length],
          ].map(([label, val]) => (
            <GlassCard key={label as string} className="text-center p-3">
              <p className="text-xs text-[#7a9bb8] uppercase tracking-widest">{label}</p>
              <p className="text-xl font-bold mt-1" style={{ color: accent }}>{val}</p>
            </GlassCard>
          ))}
        </div>
      )}

      {scans.length === 0 ? (
        <GlassCard className="text-center py-12 animate-float">
          <FileText size={40} className="mx-auto mb-3 text-[#7a9bb8]" />
          <p className="font-semibold">{portal === "user" ? "No scans yet" : "No patient records"}</p>
          <p className="text-[#7a9bb8] text-sm mt-1">{portal === "user" ? "Run an analysis to build your timeline." : "Diagnostic runs will appear here."}</p>
        </GlassCard>
      ) : (
        <GlassCard className="p-0 overflow-hidden">
          {scans.map((scan, i) => (
            <div key={scan.study_id} className={i > 0 ? "border-t border-white/[0.06]" : ""}>
              {/* Row header */}
              <button
                className="w-full flex items-center gap-3 px-4 py-3.5 hover:bg-white/[0.03] transition-colors text-left"
                onClick={() => toggle(scan.study_id)}
              >
                <span className={`flex-shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold ${scan.classification === "Malignant" ? "bg-red-500/20 text-red-300" : "bg-green-500/20 text-green-300"}`}>
                  {scan.classification}
                </span>
                <span className="flex-1 text-sm font-medium truncate">{scan.filename}</span>
                <span className="text-xs text-[#7a9bb8] hidden sm:block">{scan.model_name}</span>
                <span className="text-xs text-[#7a9bb8] hidden md:block">{new Date(scan.created_at).toLocaleDateString()}</span>
                <span className="font-mono text-xs text-[#7a9bb8]">{scan.study_id}</span>
                {scan.doctor_note && <span className="text-xs text-[#5eb3ff]">📝</span>}
                {expanded === scan.study_id ? <ChevronUp size={14} className="text-[#7a9bb8] flex-shrink-0" /> : <ChevronDown size={14} className="text-[#7a9bb8] flex-shrink-0" />}
              </button>

              {expanded === scan.study_id && <ExpandedRow scan={scan} portal={portal} />}
            </div>
          ))}
        </GlassCard>
      )}
    </div>
  )
}
