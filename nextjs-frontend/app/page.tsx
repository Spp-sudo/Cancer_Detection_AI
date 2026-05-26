"use client"

import { useRouter } from "next/navigation"
import { WebGLShader } from "@/components/ui/web-gl-shader"
import { LiquidButton } from "@/components/ui/liquid-glass-button"
import { GlassCard, MeshBackground } from "@/components/ui/glass-card"

const PILLS = [
  "Grad-CAM Explainability",
  "DICOM / Multi-modal",
  "Demo Mode",
  "Treatment Synthesis",
  "Real-time Analytics",
]

export default function Portal() {
  const router = useRouter()

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden">
      <WebGLShader />
      <MeshBackground />

      <div className="relative z-10 flex w-full max-w-4xl flex-col items-center px-4 text-center animate-fade-in">
        {/* Badge */}
        <div className="mb-6 flex items-center gap-2 rounded-full bg-[#1c1528] px-4 py-2 text-sm">
          <span className="rounded-full bg-[#5eb3ff] px-2 py-0.5 text-[0.65rem] font-bold text-black">
            AI
          </span>
          Powered Oncology Intelligence
        </div>

        {/* Logo */}
        <div className="mb-4 flex items-center gap-2 text-2xl font-bold tracking-tight">
          <span className="text-3xl">◈</span>
          OncoLens <span className="text-[#5eb3ff]">AI</span>
        </div>

        <h1 className="mb-4 text-[clamp(2rem,6vw,4rem)] font-extrabold leading-tight tracking-tight">
          Next-generation cancer care
          <br />
          intelligence
        </h1>

        <p className="mb-8 max-w-xl text-[#7a9bb8] text-lg leading-relaxed">
          Deep learning for oncology imaging — Grad-CAM explainability, DICOM support, and clinical-grade inference.
        </p>

        {/* Feature pills */}
        <div className="mb-10 flex flex-wrap justify-center gap-2">
          {PILLS.map((p) => (
            <span
              key={p}
              className="rounded-full bg-[#1c1528] px-4 py-1.5 text-sm text-white/80"
            >
              {p}
            </span>
          ))}
        </div>

        {/* Portal cards */}
        <div className="grid w-full grid-cols-1 gap-6 sm:grid-cols-2">
          <GlassCard className="flex flex-col items-start gap-3 p-7 border-[rgba(77,255,201,0.25)]">
            <span className="text-4xl">🌿</span>
            <h2 className="text-xl font-bold">Patient Demo</h2>
            <p className="text-[#7a9bb8] text-sm leading-relaxed">
              Upload scans, view AI prediction results, and receive reports in simple language.
            </p>
            <LiquidButton
              size="lg"
              className="mt-2 w-full text-white border border-[rgba(77,255,201,0.4)] rounded-full"
              onClick={() => router.push("/user/dashboard")}
            >
              Open Patient Demo →
            </LiquidButton>
          </GlassCard>

          <GlassCard className="flex flex-col items-start gap-3 p-7 border-[rgba(94,179,255,0.25)]">
            <span className="text-4xl">⚕️</span>
            <h2 className="text-xl font-bold">Clinical Demo</h2>
            <p className="text-[#7a9bb8] text-sm leading-relaxed">
              View diagnostic workflow, patient records, analytics, and AI-assisted decision support.
            </p>
            <LiquidButton
              size="lg"
              className="mt-2 w-full text-white border border-[rgba(94,179,255,0.4)] rounded-full"
              onClick={() => router.push("/doctor/dashboard")}
            >
              Open Clinical Demo →
            </LiquidButton>
          </GlassCard>
        </div>

        {/* Direct prediction button */}
        <div className="mt-8 w-full max-w-md">
          <LiquidButton
            size="lg"
            className="w-full text-white border border-[rgba(255,255,255,0.25)] rounded-full"
            onClick={() => router.push("/user/dashboard")}
          >
            Start Live AI Detection →
          </LiquidButton>
        </div>

        <p className="mt-8 text-xs text-[#7a9bb8]">
          Demo-ready architecture · Grad-CAM explainability · Render API backend
        </p>
      </div>
    </div>
  )
}
