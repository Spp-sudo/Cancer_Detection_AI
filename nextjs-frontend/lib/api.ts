const API_BASE = process.env.NEXT_PUBLIC_API_URL

if (!API_BASE) {
  throw new Error("NEXT_PUBLIC_API_URL is not set. Add your Render URL in Vercel Environment Variables.")
}

const DEMO_TOKEN = "demo_token"

async function isOnline(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`, {
      signal: AbortSignal.timeout(5000),
    })

    return res.ok
  } catch {
    return false
  }
}

async function request<T>(
  path: string,
  init?: RequestInit,
  token?: string
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init?.headers as any),
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
  })

  if (!res.ok) {
    throw new Error(await res.text())
  }

  return res.json()
}

function demoAuth(email: string, role?: string) {
  const inferredRole =
    role ?? (email.includes("doctor") || email.includes("admin") ? "doctor" : "user")

  return {
    access_token: DEMO_TOKEN,
    email,
    role: inferredRole,
  }
}

export const api = {
  login: async (email: string, _password: string) => {
    if (!(await isOnline())) {
      return demoAuth(email)
    }

    return request<{ access_token: string; email: string; role: string }>(
      "/api/v1/auth/login",
      {
        method: "POST",
        body: JSON.stringify({
          email,
          password: _password,
        }),
      }
    )
  },

  register: async (
    email: string,
    password: string,
    full_name: string,
    role = "user"
  ) => {
    if (!(await isOnline())) {
      return demoAuth(email, role)
    }

    return request<{ access_token: string; email: string; role: string }>(
      `/api/v1/auth/register?full_name=${encodeURIComponent(full_name)}&role=${role}`,
      {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
        }),
      }
    )
  },

  health: async (token?: string) => {
    if (!(await isOnline())) {
      return {
        status: "offline",
        version: "offline",
        model_name: "Render backend not reachable",
        model_loaded: false,
        database: "offline",
      }
    }

    return request<{
      status: string
      version?: string
      model_name?: string
      model_loaded?: boolean
      database?: string
      service?: string
    }>("/health", {}, token)
  },

  predict: async (
    file: File,
    token: string,
    modelName?: string
  ): Promise<PredictResult> => {
    const form = new FormData()
    form.append("image", file)

    if (modelName) {
      form.append("model_name", modelName)
    }

    const res = await fetch(`${API_BASE}/api/v1/predict`, {
      method: "POST",
      body: form,
    })

    if (!res.ok) {
      const errorText = await res.text()
      throw new Error(errorText || "Prediction failed")
    }

    return res.json()
  },

  history: async (token: string, limit = 50) => {
    return request<HistoryItem[]>(
      `/api/v1/history/scans?limit=${limit}`,
      {},
      token
    )
  },

  downloadPdf: async (studyId: string, token: string, note = "") => {
    const res = await fetch(
      `${API_BASE}/api/v1/reports/${studyId}/pdf?clinician_note=${encodeURIComponent(note)}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!res.ok) {
      throw new Error(await res.text())
    }

    return res.blob()
  },
}

export interface PredictResult {
  study_id: string
  classification: "Malignant" | "Benign"
  molecular_subtype: string
  confidence_metrics: {
    primary_confidence: number
    benign_probability: number
    malignancy_probability: number
  }
  processing_time_ms: number
  grad_cam_image_b64?: string
  recommendation: string
  evidence?: Record<string, number>
  predictions?: Array<{
    label: string
    probability: number
  }>
}

export interface HistoryItem {
  study_id: string
  filename: string
  modality: string
  classification: string
  malignancy_probability: number
  benign_probability: number
  created_at: string
  model_name?: string
}
