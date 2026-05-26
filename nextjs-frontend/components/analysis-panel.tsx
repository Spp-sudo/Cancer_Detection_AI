"use client"

import { useState, useRef } from "react"
import { Download, Upload, RotateCcw, FileText } from "lucide-react"
import { useAuth } from "@/lib/auth-context"
import { api, type PredictResult } from "@/lib/api"
import { useScanHistory } from "@/lib/scan-history"
import { generateReport } from "@/lib/report"
import { GlassCard, Eyebrow, PageTitle, MetricGrid } from "@/components/ui/glass-card"
import { LiquidButton } from "@/components/ui/liquid-glass-button"

const MODELS = [
  { label: "Brain cancer model",      hint: "Upload brain MRI or similar grayscale brain scan images." },
  { label: "Breast cancer model",     hint: "Upload breast MRI, PET, mammography, or pathology-style images." },
  { label: "Lung cancer model",       hint: "Upload lung CT or PET scan images. Natural photos are rejected." },
  { label: "Pancreatic cancer model", hint: "Upload pancreatic CT, MRI, or histopathology images." },
  { label: "Prostate cancer model",   hint: "Upload prostate MRI or prostate histopathology images." },
]

export function AnalysisPanel({ portal }: { portal: "user" | "doctor" }) {
  const { token } = useAuth()
  const { addScan } = useScanHistory()
  const accent = portal === "user" ? "#4dffc9" : "#5eb3ff"
  const [file, setFile] = useState<File | null>(null)
  const [model, setModel] = useState(MODELS[0].label)
  const [note, setNote] = useState("")
  const [result, setResult] = useState<PredictResult | null>(null)
  const [filename, setFilename] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const inputRef = useRef<HTMLInputElement>(null)

  const hint = MODELS.find(m => m.label === model)?.hint ?? ""
  const isMalignant = result?.classification === "Malignant"
  const resultAccent = isMalignant ? "#ff6b8a" : "#4dffc9"

  const run = async () => {
    if (!file || !token) return
    setLoading(true); setError(""); setResult(null)
    try {
      const r = await api.predict(file, token, model)
      setResult(r)
      setFilename(file.name)
      addScan({ ...r, filename: file.name, model_name: model, created_at: new Date().toISOString() })
    } catch (e: any) {
      setError(e.message ?? "Analysis failed")
    } finally { setLoading(false) }
  }

  const downloadReport = () => {
    if (!result) return
    const text = generateReport(result, filename, note, "", portal)
    const blob = new Blob([text], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `oncolens_report_${result.study_id}_${Date.now()}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="flex flex-col gap-6 max-w-3xl">
      <div>
        <Eyebrow accent={accent}>{portal === "user" ? "Step 1 · Upload" : "Diagnostics"}</Eyebrow>
        <PageTitle accent={accent}>{portal === "user" ? "Share your scan" : "Upload Imaging Study"}</PageTitle>
        <p className="text-[#7a9bb8] text-sm">{portal === "user" ? "Upload your medical imaging study for AI analysis." : "Upload patient imaging and provide clinical context."}</p>
      </div>

      {!result ? (
        <div className="grid gap-6 md:grid-cols-2">
          {/* Upload zone */}
          <GlassCard
            className="flex flex-col items-center justify-center gap-3 p-8 border-dashed border-[rgba(0,200,255,0.35)] cursor-pointer hover:border-[rgba(0,212,255,0.6)] transition-colors min-h-[200px]"
            onClick={() => inputRef.current?.click()}
          >
            <Upload size={32} className="text-[#7a9bb8]" />
            <p className="font-semibold text-center text-sm">{file ? file.name : "Click to select scan"}</p>
            <p className="text-xs text-[#7a9bb8] text-center">PNG · JPEG · TIFF · BMP · DICOM</p>
            {file && <span className="rounded-full bg-[rgba(77,255,201,0.15)] px-3 py-1 text-xs text-[#4dffc9]">✓ Ready</span>}
            <input ref={inputRef} type="file" accept=".png,.jpg,.jpeg,.tiff,.tif,.bmp,.dcm" className="hidden"
              onChange={e => setFile(e.target.files?.[0] ?? null)} />
          </GlassCard>

          {/* Context */}
          <GlassCard className="flex flex-col gap-3">
            <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: accent }}>
              {portal === "user" ? "Clinical context" : "Clinical intake"}
            </p>
            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">AI Model</label>
              <select className="rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm outline-none focus:border-[#5eb3ff]"
                value={model} onChange={e => setModel(e.target.value)}>
                {MODELS.map(m => <option key={m.label} value={m.label}>{m.label}</option>)}
              </select>
              <p className="text-xs text-[#7a9bb8]">{hint}</p>
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">{portal === "user" ? "Describe your concern (optional)" : "Attending notes (optional)"}</label>
              <textarea className="rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm outline-none focus:border-[#5eb3ff] resize-none"
                rows={3} placeholder={portal === "user" ? "Symptoms, history, concerns…" : "Clinical observations, suspected diagnosis…"}
                value={note} onChange={e => setNote(e.target.value)} />
            </div>
            <LiquidButton size="lg" className="w-full text-white rounded-full" style={{ border: `1px solid ${accent}66` }}
              onClick={run} disabled={!file || loading}>
              {loading
                ? <span className="flex items-center gap-2"><span className="h-4 w-4 rounded-full border-2 border-white/30 border-t-white animate-spin" />Analyzing…</span>
                : portal === "user" ? "✨ Start AI Health Analysis" : "🚀 Run Diagnostic Pipeline"}
            </LiquidButton>
          </GlassCard>
        </div>
      ) : (
        /* ── Results ── */
        <div className="flex flex-col gap-4 animate-fade-in">
          {/* Classification banner */}
          <GlassCard style={{ borderColor: `${resultAccent}44` }}>
            <p className="text-xs uppercase tracking-widest text-[#7a9bb8] mb-1">Analysis Complete</p>
            <h2 className="text-3xl font-bold" style={{ color: resultAccent }}>{result.classification}</h2>
            <p className="text-[#7a9bb8] text-sm mt-1">{result.study_id} · {result.molecular_subtype}</p>
          </GlassCard>

          <MetricGrid items={[
            ["Confidence", `${(result.confidence_metrics.primary_confidence * 100).toFixed(0)}%`],
            ["Benign",     `${(result.confidence_metrics.benign_probability * 100).toFixed(0)}%`],
            ["Malignant",  `${(result.confidence_metrics.malignancy_probability * 100).toFixed(0)}%`],
            ["Speed",      `${result.processing_time_ms.toFixed(0)}ms`],
          ]} />

          {/* Condition description */}
          <GlassCard>
            <p className="text-sm font-semibold mb-2 flex items-center gap-2">
              <FileText size={14} style={{ color: accent }} /> Condition Description
            </p>
            <p className="text-[#7a9bb8] text-sm leading-relaxed">{result.recommendation}</p>
            {result.molecular_subtype && (
              <p className="mt-2 text-xs text-[#7a9bb8]">
                <span className="font-semibold text-white">Detected:</span> {result.molecular_subtype}
              </p>
            )}
          </GlassCard>

          {/* Top predictions */}
          {result.predictions && result.predictions.length > 0 && (
            <GlassCard>
              <p className="text-sm font-semibold mb-3">Top Predictions</p>
              <div className="flex flex-col gap-2">
                {result.predictions.slice(0, 5).map(p => (
                  <div key={p.label} className="flex items-center gap-3">
                    <span className="w-40 text-xs text-[#7a9bb8] truncate">{p.label.replace(/_/g, " ")}</span>
                    <div className="flex-1 h-1.5 rounded-full bg-white/10 overflow-hidden">
                      <div className="h-full rounded-full transition-all" style={{ width: `${p.probability * 100}%`, background: accent }} />
                    </div>
                    <span className="text-xs w-10 text-right">{(p.probability * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}

          {/* Report download */}
          <GlassCard className="flex flex-col gap-3">
            <p className="text-sm font-semibold">📄 Professional Report</p>
            <p className="text-xs text-[#7a9bb8]">Full diagnostic report including condition description, AI findings, evidence features, and clinical recommendations.</p>
            <div className="flex gap-3">
              <button
                onClick={downloadReport}
                className="flex items-center gap-2 rounded-xl border border-white/20 bg-white/5 px-4 py-2.5 text-sm font-medium hover:bg-white/10 transition-colors"
              >
                <Download size={14} /> Download TXT Report
              </button>
            </div>
          </GlassCard>

          <button className="flex items-center gap-2 text-xs text-[#7a9bb8] hover:text-white"
            onClick={() => { setResult(null); setFile(null); setNote("") }}>
            <RotateCcw size={12} /> Upload another scan
          </button>
        </div>
      )}

      {error && <p className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-sm text-red-400">{error}</p>}
    </div>
  )
}
