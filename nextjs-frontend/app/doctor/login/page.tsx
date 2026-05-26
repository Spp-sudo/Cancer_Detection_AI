"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Eye, EyeOff, Loader2, Activity } from "lucide-react"
import { useAuth } from "@/lib/auth-context"
import { api } from "@/lib/api"
import { GlassCard, MeshBackground, Eyebrow, PageTitle } from "@/components/ui/glass-card"
import { LiquidButton } from "@/components/ui/liquid-glass-button"

const STATS = [
  ["Diagnostics pipeline", "94%"],
  ["Patient records DB",   "88%"],
  ["Report generation",    "96%"],
  ["Model accuracy",       "91%"],
]

export default function DoctorLogin() {
  const router = useRouter()
  const { setAuth } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [show, setShow] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true); setError("")
    try {
      const data = await api.login(email || "doctor@oncolens.ai", password || "doctor123")
      setAuth({ token: data.access_token, email: data.email, role: data.role, portal: "doctor" })
      router.push("/doctor/dashboard")
    } catch {
      setError("Authentication failed. Use the demo credentials below.")
    } finally { setLoading(false) }
  }

  const demoLogin = async () => {
    setLoading(true); setError("")
    try {
      const data = await api.login("doctor@oncolens.ai", "doctor123")
      setAuth({ token: data.access_token, email: data.email, role: data.role, portal: "doctor" })
      router.push("/doctor/dashboard")
    } finally { setLoading(false) }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4">
      <MeshBackground />
      <div className="relative z-10 grid w-full max-w-4xl gap-10 md:grid-cols-2 animate-fade-in">

        {/* Left */}
        <div className="flex flex-col justify-center gap-5">
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[rgba(94,179,255,0.15)]">
              <Activity size={16} color="#5eb3ff" />
            </span>
            <span className="text-xs font-semibold uppercase tracking-widest text-[#5eb3ff]">Clinical Portal</span>
          </div>
          <Eyebrow accent="#5eb3ff">Clinical intelligence workstation</Eyebrow>
          <PageTitle accent="#5eb3ff">OncoLens Pro</PageTitle>
          <p className="text-[#7a9bb8] text-sm leading-relaxed">Enterprise-grade AI diagnostics, patient records, and real-time analytics for clinical teams.</p>

          <div className="grid grid-cols-2 gap-3">
            {[["< 2s","Inference"],["Grad-CAM","Explainability"],["JWT","Auth"],["PDF","Reports"]].map(([val, label]) => (
              <div key={label} className="rounded-xl border border-white/[0.06] bg-white/[0.03] p-3 text-center">
                <p className="text-lg font-bold text-[#5eb3ff]">{val}</p>
                <p className="text-xs text-[#7a9bb8]">{label}</p>
              </div>
            ))}
          </div>

          <GlassCard className="animate-float">
            <p className="text-xs text-[#7a9bb8] mb-3 uppercase tracking-widest">System status</p>
            {STATS.map(([label, pct]) => (
              <div key={label} className="mb-3 last:mb-0">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-[#7a9bb8]">{label}</span>
                  <span className="text-[#5eb3ff]">{pct}</span>
                </div>
                <div className="h-1 rounded-full bg-white/10 overflow-hidden">
                  <div className="h-full rounded-full bg-gradient-to-r from-[#5eb3ff] to-[#00d4ff] transition-all duration-1000" style={{ width: pct }} />
                </div>
              </div>
            ))}
          </GlassCard>
        </div>

        {/* Right */}
        <GlassCard className="flex flex-col gap-4">
          <div>
            <Eyebrow accent="#5eb3ff">Physician access</Eyebrow>
            <h3 className="text-xl font-bold">Clinical sign in</h3>
            <p className="text-xs text-[#7a9bb8] mt-1">Authorized medical staff only</p>
          </div>

          <form onSubmit={submit} className="flex flex-col gap-3">
            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Institutional email</label>
              <input
                className="rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm outline-none focus:border-[#5eb3ff] transition-colors"
                placeholder="doctor@hospital.org"
                value={email} onChange={e => setEmail(e.target.value)}
              />
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Password</label>
              <div className="relative">
                <input
                  type={show ? "text" : "password"}
                  className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 pr-10 text-sm outline-none focus:border-[#5eb3ff] transition-colors"
                  placeholder="••••••••"
                  value={password} onChange={e => setPassword(e.target.value)}
                />
                <button type="button" onClick={() => setShow(s => !s)} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#7a9bb8] hover:text-white">
                  {show ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {error && <p className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-xs text-red-400">{error}</p>}

            <LiquidButton size="lg" className="w-full text-white border border-[rgba(94,179,255,0.4)] rounded-full" type="submit" disabled={loading}>
              {loading ? <span className="flex items-center gap-2"><Loader2 size={14} className="animate-spin" />Authenticating…</span> : "Authenticate"}
            </LiquidButton>
          </form>

          {/* Demo hint */}
          <div className="rounded-xl border border-[rgba(94,179,255,0.2)] bg-[rgba(94,179,255,0.05)] px-4 py-3">
            <p className="text-xs text-[#5eb3ff] font-semibold mb-1">🔑 Demo credentials</p>
            <p className="text-xs text-[#7a9bb8]">doctor@oncolens.ai / doctor123</p>
            <button onClick={demoLogin} className="mt-2 text-xs text-[#5eb3ff] underline underline-offset-2 hover:text-white">
              Click to auto-fill & sign in →
            </button>
          </div>

          <div className="border-t border-white/[0.06] pt-3 text-center text-sm text-[#7a9bb8]">
            New to OncoLens?{" "}
            <button className="text-[#5eb3ff] font-semibold hover:underline" onClick={() => router.push("/doctor/register")}>Register practice →</button>
          </div>
          <button className="text-xs text-[#7a9bb8] hover:text-white" onClick={() => router.push("/")}>← Back to portal</button>
        </GlassCard>
      </div>
    </div>
  )
}
