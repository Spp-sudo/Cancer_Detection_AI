import { NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import { writeFile, unlink } from "fs/promises"
import { join } from "path"
import { tmpdir } from "os"
import { randomUUID } from "crypto"

// next dev/build runs from nextjs-frontend/, so project root is one level up
const PROJECT_ROOT = join(process.cwd(), "..")
const PYTHON = join(PROJECT_ROOT, ".venv", "bin", "python3")
const SCRIPT = join(PROJECT_ROOT, "predict_json.py")

export async function POST(req: NextRequest) {
  const form = await req.formData()
  const file = form.get("image") as File | null
  const modelName = (form.get("model_name") as string) ?? "Brain cancer model"

  if (!file) return NextResponse.json({ error: "No image provided" }, { status: 400 })

  const ext = file.name.split(".").pop() ?? "png"
  const tmpPath = join(tmpdir(), `oncolens_${randomUUID()}.${ext}`)
  await writeFile(tmpPath, Buffer.from(await file.arrayBuffer()))

  try {
    const output = await new Promise<string>((resolve, reject) => {
      const proc = spawn(PYTHON, [SCRIPT, tmpPath, "--model-name", modelName], {
        cwd: PROJECT_ROOT,
      })
      let out = ""
      let err = ""
      proc.stdout.on("data", (d: Buffer) => (out += d.toString()))
      proc.stderr.on("data", (d: Buffer) => (err += d.toString()))
      proc.on("close", code => {
        if (code !== 0) reject(new Error(err.split("\n").slice(-3).join(" ") || `Python exited ${code}`))
        else resolve(out.trim())
      })
    })
    return NextResponse.json(JSON.parse(output))
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 })
  } finally {
    await unlink(tmpPath).catch(() => {})
  }
}
