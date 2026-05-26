"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Eye, EyeOff, Loader2, CheckCircle2 } from "lucide-react"
import { useAuth } from "@/lib/auth-context"
import { api } from "@/lib/api"
import { GlassCard, MeshBackground, Eyebrow } from "@/components/ui/glass-card"
import { LiquidButton } from "@/components/ui/liquid-glass-button"

export default function UserRegister() {
  const router = useRouter()
  const { setAuth } = useAuth()
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" })
  const [showPw, setShowPw] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const pwStrength = form.password.length === 0 ? 0 : form.password.length < 6 ? 1 : form.password.length < 10 ? 2 : 3
  const strengthLabel = ["", "Weak", "Good", "Strong"][pwStrength]
  const strengthColor = ["", "#ff6b8a", "#ffb86b", "#4dffc9"][pwStrength]

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.name || !form.email || !form.password) return setError("All fields are required.")
    if (form.password !== form.confirm) return setError("Passwords do not match.")
    if (form.password.length < 6) return setError("Password must be at least 6 characters.")
    setLoading(true); setError("")
    try {
      const data = await api.register(form.email, form.password, form.name, "user")
      setAuth({ token: data.access_token, email: data.email, role: "user", portal: "user" })
      router.push("/user/dashboard")
    } catch (e: any) {
      setError(e.message ?? "Registration failed.")
    } finally { setLoading(false) }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4 py-10">
      <MeshBackground />
      <div className="relative z-10 grid w-full max-w-4xl gap-8 md:grid-cols-2 animate-fade-in">

        <GlassCard className="flex flex-col gap-4">
          <div>
            <Eyebrow accent="#4dffc9">Create account</Eyebrow>
            <h3 className="text-xl font-bold">Patient registration</h3>
            <p className="text-xs text-[#7a9bb8] mt-1">Free forever. No credit card required.</p>
          </div>

          <form onSubmit={submit} className="flex flex-col gap-3">
            {[
              { key: "name",  label: "Full name",  placeholder: "Jane Smith",          type: "text" },
              { key: "email", label: "Email",       placeholder: "jane@example.com",    type: "email" },
            ].map(({ key, label, placeholder, type }) => (
              <div key={key} className="flex flex-col gap-1">
                <label className="text-xs text-[#7a9bb8]">{label}</label>
                <input type={type} className="rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm outline-none focus:border-[#4dffc9] transition-colors"
                  placeholder={placeholder} value={(form as any)[key]} onChange={e => setForm(p => ({ ...p, [key]: e.target.value }))} />
              </div>
            ))}

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Password</label>
              <div className="relative">
                <input type={showPw ? "text" : "password"} className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 pr-10 text-sm outline-none focus:border-[#4dffc9] transition-colors"
                  placeholder="Create a secure password" value={form.password} onChange={e => setForm(p => ({ ...p, password: e.target.value }))} />
                <button type="button" onClick={() => setShowPw(s => !s)} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#7a9bb8] hover:text-white">
                  {showPw ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
              {form.password && (
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex gap-1 flex-1">
                    {[1,2,3].map(i => <div key={i} className="h-1 flex-1 rounded-full transition-all" style={{ background: i <= pwStrength ? strengthColor : "rgba(255,255,255,0.1)" }} />)}
                  </div>
                  <span className="text-xs" style={{ color: strengthColor }}>{strengthLabel}</span>
                </div>
              )}
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Confirm password</label>
              <div className="relative">
                <input type={showPw ? "text" : "password"} className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 pr-10 text-sm outline-none focus:border-[#4dffc9] transition-colors"
                  placeholder="Re-enter password" value={form.confirm} onChange={e => setForm(p => ({ ...p, confirm: e.target.value }))} />
                {form.confirm && form.confirm === form.password && (
                  <CheckCircle2 size={15} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4dffc9]" />
                )}
              </div>
            </div>

            {error && <p className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-xs text-red-400">{error}</p>}

            <LiquidButton size="lg" className="w-full text-white border border-[rgba(77,255,201,0.4)] rounded-full" type="submit" disabled={loading}>
              {loading ? <span className="flex items-center gap-2"><Loader2 size={14} className="animate-spin" />Creating…</span> : "Create my account"}
            </LiquidButton>
          </form>

          <div className="border-t border-white/[0.06] pt-3 text-center text-sm text-[#7a9bb8]">
            Already have an account?{" "}
            <button className="text-[#4dffc9] font-semibold hover:underline" onClick={() => router.push("/user/login")}>Sign in →</button>
          </div>
        </GlassCard>

        <div className="flex flex-col gap-3 justify-center">
          <Eyebrow accent="#4dffc9">Why join OncoLens?</Eyebrow>
          {[
            ["🫁", "AI-Powered Analysis",      "Advanced deep learning models analyze your medical imaging with clinical-grade accuracy."],
            ["🔬", "Grad-CAM Explainability",  "Understand what the AI focuses on with heatmap visualizations of your scans."],
            ["📄", "Downloadable Reports",     "Professional TXT reports with full diagnosis details and recommendations."],
            ["🔒", "Secure & Private",         "HIPAA-aware architecture with JWT authentication and encrypted transmission."],
          ].map(([icon, title, desc]) => (
            <GlassCard key={title} className="flex items-start gap-3 p-4">
              <span className="text-2xl flex-shrink-0">{icon}</span>
              <div>
                <p className="font-semibold text-sm">{title}</p>
                <p className="text-[#7a9bb8] text-xs mt-0.5">{desc}</p>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </div>
  )
}
