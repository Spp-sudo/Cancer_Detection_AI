import { cn } from "@/lib/utils"

export function GlassCard({ children, className, floating, ...props }: React.HTMLAttributes<HTMLDivElement> & { floating?: boolean }) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-[rgba(120,200,255,0.18)] bg-[rgba(12,28,48,0.55)] backdrop-blur-xl",
        "shadow-[0_8px_32px_rgba(0,0,0,0.35)] p-5",
        "transition-all duration-300 hover:-translate-y-0.5 hover:border-[rgba(0,212,255,0.35)]",
        floating && "animate-float",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export function MeshBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden" aria-hidden>
      <div className="absolute -top-[15%] -left-[10%] h-[55vw] w-[55vw] rounded-full bg-[radial-gradient(circle,rgba(0,180,255,0.12),transparent_70%)] blur-[80px]" />
      <div className="absolute -bottom-[10%] -right-[5%] h-[45vw] w-[45vw] rounded-full bg-[radial-gradient(circle,rgba(100,80,255,0.10),transparent_70%)] blur-[80px]" />
    </div>
  )
}

export function Eyebrow({ children, accent = "#5eb3ff" }: { children: React.ReactNode; accent?: string }) {
  return (
    <p className="mb-1 text-[0.72rem] font-semibold uppercase tracking-[0.2em]" style={{ color: accent }}>
      {children}
    </p>
  )
}

export function PageTitle({ children, accent = "#5eb3ff" }: { children: React.ReactNode; accent?: string }) {
  return (
    <h1
      className="mb-2 font-bold tracking-tight leading-tight text-[clamp(1.5rem,3vw,2rem)]"
      style={{ background: `linear-gradient(135deg,#fff,${accent})`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}
    >
      {children}
    </h1>
  )
}

export function MetricGrid({ items }: { items: [string, string][] }) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 my-4">
      {items.map(([label, value]) => (
        <div key={label} className="rounded-xl border border-white/[0.08] bg-black/25 p-3 text-center">
          <p className="text-[0.68rem] uppercase tracking-widest text-[#7a9bb8]">{label}</p>
          <p className="mt-1 font-semibold text-[1.2rem] text-[#00e6c3]">{value}</p>
        </div>
      ))}
    </div>
  )
}
