"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Eye, EyeOff, Loader2, CheckCircle2 } from "lucide-react"
import { useAuth } from "@/lib/auth-context"
import { api } from "@/lib/api"
import { GlassCard, MeshBackground, Eyebrow } from "@/components/ui/glass-card"
import { LiquidButton } from "@/components/ui/liquid-glass-button"

export default function DoctorRegister() {
  const router = useRouter()
  const { setAuth } = useAuth()
  const [form, setForm] = useState({ name: "", hospital: "", email: "", password: "", confirm: "" })
  const [showPw, setShowPw] = useState(false)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const pwStrength = form.password.length === 0 ? 0 : form.password.length < 6 ? 1 : form.password.length < 10 ? 2 : 3
  const strengthColor = ["", "#ff6b8a", "#ffb86b", "#5eb3ff"][pwStrength]

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.name || !form.email || !form.password) return setError("All fields are required.")
    if (form.password !== form.confirm) return setError("Passwords do not match.")
    if (form.password.length < 6) return setError("Password must be at least 6 characters.")
    setLoading(true); setError("")
    try {
      const data = await api.register(form.email, form.password, form.name, "doctor")
      setAuth({ token: data.access_token, email: data.email, role: "doctor", portal: "doctor" })
      router.push("/doctor/dashboard")
    } catch (e: any) {
      setError(e.message ?? "Registration failed.")
    } finally { setLoading(false) }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4 py-10">
      <MeshBackground />
      <div className="relative z-10 grid w-full max-w-4xl gap-8 md:grid-cols-2 animate-fade-in">

        <div className="flex flex-col gap-3 justify-center">
          <Eyebrow accent="#5eb3ff">Clinical workstation</Eyebrow>
          {[
            ["⚕️", "Enterprise Diagnostics",  "Multi-modal inference engine supporting CT, MRI, X-ray, and DICOM."],
            ["🎯", "Real-time Analytics",      "Dashboard with patient metrics, trend analysis, and population health insights."],
            ["📋", "Patient Management",       "Comprehensive records with treatment synthesis and downloadable reports."],
            ["🛡️", "HIPAA Compliant",          "Enterprise-grade security with JWT auth, audit logging, and role-based access."],
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

        <GlassCard className="flex flex-col gap-4">
          <div>
            <Eyebrow accent="#5eb3ff">Register practice</Eyebrow>
            <h3 className="text-xl font-bold">Physician registration</h3>
            <p className="text-xs text-[#7a9bb8] mt-1">Authorized medical staff only. Institutional verification required.</p>
          </div>

          <form onSubmit={submit} className="flex flex-col gap-3">
            {[
              { key: "name",     label: "Full name",           placeholder: "Dr. Sarah Chen",          type: "text" },
              { key: "hospital", label: "Institution",         placeholder: "City Medical Center",     type: "text" },
              { key: "email",    label: "Institutional email", placeholder: "sarah@hospital.org",      type: "email" },
            ].map(({ key, label, placeholder, type }) => (
              <div key={key} className="flex flex-col gap-1">
                <label className="text-xs text-[#7a9bb8]">{label}</label>
                <input type={type} className="rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm outline-none focus:border-[#5eb3ff] transition-colors"
                  placeholder={placeholder} value={(form as any)[key]} onChange={e => setForm(p => ({ ...p, [key]: e.target.value }))} />
              </div>
            ))}

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Password</label>
              <div className="relative">
                <input type={showPw ? "text" : "password"} className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 pr-10 text-sm outline-none focus:border-[#5eb3ff] transition-colors"
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
                  <span className="text-xs" style={{ color: strengthColor }}>{["","Weak","Good","Strong"][pwStrength]}</span>
                </div>
              )}
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs text-[#7a9bb8]">Confirm password</label>
              <div className="relative">
                <input type={showPw ? "text" : "password"} className="w-full rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 pr-10 text-sm outline-none focus:border-[#5eb3ff] transition-colors"
                  placeholder="Re-enter password" value={form.confirm} onChange={e => setForm(p => ({ ...p, confirm: e.target.value }))} />
                {form.confirm && form.confirm === form.password && (
                  <CheckCircle2 size={15} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#5eb3ff]" />
                )}
              </div>
            </div>

            {error && <p className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 text-xs text-red-400">{error}</p>}

            <LiquidButton size="lg" className="w-full text-white border border-[rgba(94,179,255,0.4)] rounded-full" type="submit" disabled={loading}>
              {loading ? <span className="flex items-center gap-2"><Loader2 size={14} className="animate-spin" />Registering…</span> : "Register practice"}
            </LiquidButton>
          </form>

          <div className="border-t border-white/[0.06] pt-3 text-center text-sm text-[#7a9bb8]">
            Already registered?{" "}
            <button className="text-[#5eb3ff] font-semibold hover:underline" onClick={() => router.push("/doctor/login")}>Sign in →</button>
          </div>
        </GlassCard>
      </div>
    </div>
  )
}
