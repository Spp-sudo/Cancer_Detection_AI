"use client"

import { createContext, useContext, useState, ReactNode } from "react"

interface AuthState {
  token: string | null
  email: string | null
  role: string | null
  portal: "user" | "doctor" | null
}

interface AuthCtx extends AuthState {
  setAuth: (s: Partial<AuthState>) => void
  logout: () => void
}

const Ctx = createContext<AuthCtx | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({ token: null, email: null, role: null, portal: null })

  const setAuth = (s: Partial<AuthState>) => setState(p => ({ ...p, ...s }))
  const logout = () => setState({ token: null, email: null, role: null, portal: null })

  return <Ctx.Provider value={{ ...state, setAuth, logout }}>{children}</Ctx.Provider>
}

export function useAuth() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error("useAuth must be inside AuthProvider")
  return ctx
}
