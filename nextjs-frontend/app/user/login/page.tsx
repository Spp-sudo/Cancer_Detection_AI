"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Eye, EyeOff, Loader2, Stethoscope } from "lucide-react"
import { useAuth } from "@/lib/auth-context"
import { api } from "@/lib/api"
import { GlassCard, MeshBackground, Eyebrow, PageTitle } from "@/components/ui/glass-card"
import { LiquidButton } from "@/components/ui/liquid-glass-button"

export default function UserLogin() {
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
      const data = await api.login(email || "user@oncolens.ai", password || "user123")
      setAuth({ token: data.access_token, email: data.email, role: data.role, portal: "user" })
      router.push("/user/dashboard")
    } catch {
      setError("Sign in failed. Use the demo credentials below.")
    } finally { setLoading(false) }
  }

  const demoLogin = async () => {
    setLoading(true); setError("")
    try {
      const data = await api.login("user@oncolens.ai", "user123")
      setAuth({ token: data.access_token, email: data.email, role: data.role, portal: "user" })
      router.push("/user/dashboard")
    } finally { setLoading(false) }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4">
      <MeshBackground />
      <div className="relative z-10 grid w-full max-w-4xl gap-10 md:grid-cols-2 animate-fade-in">

        {/* Left */}
        <div className="flex flex-col justify-center gap-5">
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[rgba(77,255,201,0.15)]">
              <Stethoscope size={16} color="#4dffc9" />
            </span>
            <span className="text-xs font-semibold uppercase tracking-widest text-[#4dffc9]">Patient Portal</span>
          </div>
          <Eyebrow accent="#4dffc9">Your health companion</Eyebrow>
          <PageTitle accent="#4dffc9">Welcome to OncoLens</PageTitle>
          <p className="text-[#7a9bb8] leading-relaxed text-sm">AI-powered medical imaging analysis — calmly, clearly, and securely.</p>

          <div className="flex flex-col gap-2">
            {[
              ["📤", "Upload your scan", "PNG, JPEG, TIFF, DICOM supported"],
              ["🤖", "AI-powered analysis", "Deep learning inference in seconds"],
              ["📊", "Track your history", "Full timeline of all your scans"],
              ["📄", "Download reports", "Professional PDF & TXT reports"],
            ].map(([icon, title, sub]) => (
              <div key={title} className="flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.03] px-4 py-3">
                <span className="text-xl">{icon}</span>
                <div>
                  <p className="text-sm font-medium text-white">{title}</p>
                  <p className="text-xs text-[#7a9bb8]">{sub}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right */}
        <GlassCard className="flex flex-col gap-4">
          <div>
            <Eyebrow accent="#4dffc9">Patient sign in</Eyebrow>
            <h3 className="text-xl font-bold">Access your dashboard</h3>
          </div>

          <form onSubmit={submit} className="flex flex-col gap-3">
            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Email</label>
              <input
                className="rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm outline-none focus:border-[#4dffc9] transition-colors"
                placeholder="you@example.com"
                value={email} onChange={e => setEmail(e.target.value)}
              />
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Password</label>
              <div className="relative">
                <input
                  type={show ? "text" : "password"}
                  className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 pr-10 text-sm outline-none focus:border-[#4dffc9] transition-colors"
                  placeholder="••••••••"
                  value={password} onChange={e => setPassword(e.target.value)}
                />
                <button type="button" onClick={() => setShow(s => !s)} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#7a9bb8] hover:text-white">
                  {show ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {error && <p className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-xs text-red-400">{error}</p>}

            <LiquidButton size="lg" className="w-full text-white border border-[rgba(77,255,201,0.4)] rounded-full" type="submit" disabled={loading}>
              {loading ? <span className="flex items-center gap-2"><Loader2 size={14} className="animate-spin" />Signing in…</span> : "Continue to my dashboard"}
            </LiquidButton>
          </form>

          {/* Demo hint */}
          <div className="rounded-xl border border-[rgba(77,255,201,0.2)] bg-[rgba(77,255,201,0.05)] px-4 py-3">
            <p className="text-xs text-[#4dffc9] font-semibold mb-1">🚀 Demo credentials</p>
            <p className="text-xs text-[#7a9bb8]">user@oncolens.ai / user123</p>
            <button onClick={demoLogin} className="mt-2 text-xs text-[#4dffc9] underline underline-offset-2 hover:text-white">
              Click to auto-fill & sign in →
            </button>
          </div>

          <div className="border-t border-white/[0.06] pt-3 text-center text-sm text-[#7a9bb8]">
            No account?{" "}
            <button className="text-[#4dffc9] font-semibold hover:underline" onClick={() => router.push("/user/register")}>Create one →</button>
          </div>
          <button className="text-xs text-[#7a9bb8] hover:text-white" onClick={() => router.push("/")}>← Back to portal</button>
        </GlassCard>
      </div>
    </div>
  )
}
