import type { PredictResult } from "./api"

const CONDITION_DESCRIPTIONS: Record<string, string> = {
  brain_cancer:      "Brain cancer refers to abnormal cell growth within the brain tissue. Common types include glioblastoma, meningioma, and astrocytoma. Symptoms may include headaches, seizures, cognitive changes, and neurological deficits.",
  breast_cancer:     "Breast cancer originates in breast tissue, most commonly in the ducts or lobules. It is one of the most prevalent cancers worldwide. Early detection significantly improves prognosis.",
  lung_cancer:       "Lung cancer is the leading cause of cancer-related mortality. It is classified as non-small cell (NSCLC) or small cell (SCLC). Risk factors include smoking, radon exposure, and occupational hazards.",
  pancreatic_cancer: "Pancreatic cancer arises from the exocrine or endocrine cells of the pancreas. It is often diagnosed at an advanced stage due to the absence of early symptoms, making it one of the most challenging cancers to treat.",
  prostate_cancer:   "Prostate cancer develops in the prostate gland. It is the most common cancer in men. Many cases are slow-growing, but aggressive forms require prompt treatment including surgery, radiation, or hormone therapy.",
  no_cancer:         "No malignant patterns were detected in this imaging study. The scan appears within normal limits for the selected model. Routine follow-up is recommended as per clinical guidelines.",
  cancer:            "The imaging study shows patterns consistent with malignant cell activity. Further histopathological confirmation is required to determine the specific cancer type and staging.",
}

const RECOMMENDATIONS: Record<string, string[]> = {
  Malignant: [
    "Immediate referral to an oncology specialist is strongly recommended.",
    "Histopathological biopsy should be performed to confirm diagnosis and determine cancer subtype.",
    "Staging workup including PET-CT or MRI may be required to assess disease extent.",
    "Multidisciplinary tumor board review is advised before initiating treatment.",
    "Patient should be counseled regarding diagnosis, treatment options, and prognosis.",
  ],
  Benign: [
    "No immediate intervention required based on current imaging findings.",
    "Routine clinical follow-up in 6–12 months is recommended.",
    "Patient should be advised to report any new or worsening symptoms promptly.",
    "Lifestyle modifications including diet, exercise, and smoking cessation are encouraged.",
    "Annual screening as per age-appropriate clinical guidelines is advised.",
  ],
}

export function generateReport(result: PredictResult, filename: string, patientNote: string, doctorNote: string, portal: "user" | "doctor"): string {
  const now = new Date()
  const ts = now.toISOString().replace("T", " ").slice(0, 19) + " UTC"
  const date = now.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })

  const subtype = result.molecular_subtype?.toLowerCase().replace(/ /g, "_") ?? ""
  const conditionKey = Object.keys(CONDITION_DESCRIPTIONS).find(k => subtype.includes(k)) ?? (result.classification === "Malignant" ? "cancer" : "no_cancer")
  const conditionDesc = CONDITION_DESCRIPTIONS[conditionKey] ?? "No additional description available."
  const recs = RECOMMENDATIONS[result.classification] ?? RECOMMENDATIONS.Benign

  const cm = result.confidence_metrics
  const topPreds = (result.predictions ?? []).slice(0, 5).map(p =>
    `  • ${p.label.replace(/_/g, " ").padEnd(30)} ${(p.probability * 100).toFixed(1)}%`
  ).join("\n")

  const evidenceLines = result.evidence
    ? Object.entries(result.evidence).map(([k, v]) =>
        `  • ${k.replace(/_/g, " ").padEnd(30)} ${(v as number).toFixed(4)}`
      ).join("\n")
    : "  Not available"

  const separator = "═".repeat(60)
  const thin = "─".repeat(60)

  return `${separator}
  ONCOLENS AI — CLINICAL DIAGNOSTIC REPORT
  Educational prototype only. Not for clinical diagnosis.
${separator}

  Report Generated : ${ts}
  Report Date      : ${date}
  Study ID         : ${result.study_id}
  Image File       : ${filename}
  Portal           : ${portal === "doctor" ? "Clinical (Physician)" : "Patient"}

${thin}
  DIAGNOSIS SUMMARY
${thin}

  Classification   : ${result.classification.toUpperCase()}
  Detected Type    : ${result.molecular_subtype}
  Confidence       : ${(cm.primary_confidence * 100).toFixed(1)}%
  Benign Prob.     : ${(cm.benign_probability * 100).toFixed(1)}%
  Malignant Prob.  : ${(cm.malignancy_probability * 100).toFixed(1)}%
  Processing Time  : ${result.processing_time_ms.toFixed(0)} ms

${thin}
  CONDITION DESCRIPTION
${thin}

${conditionDesc.match(/.{1,58}/g)?.map(l => `  ${l}`).join("\n")}

${thin}
  AI RECOMMENDATIONS
${thin}

${recs.map((r, i) => `  ${i + 1}. ${r}`).join("\n")}

${thin}
  TOP PREDICTIONS
${thin}

${topPreds || "  Not available"}

${thin}
  IMAGE EVIDENCE FEATURES
${thin}

${evidenceLines}

${patientNote ? `${thin}
  PATIENT NOTES
${thin}

  ${patientNote}

` : ""}${doctorNote ? `${thin}
  PHYSICIAN NOTES
${thin}

  ${doctorNote}

` : ""}${separator}
  DISCLAIMER
${separator}

  This report is generated by an AI system for educational and
  research purposes only. It is NOT a substitute for professional
  medical advice, diagnosis, or treatment. Always consult a
  qualified healthcare provider for medical decisions.

  OncoLens AI · ${date}
${separator}
`
}
