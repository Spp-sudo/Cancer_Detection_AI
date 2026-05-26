from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Cancer Detection API is running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "cancer-detection-api",
        "model_loaded": True
    }

@app.post("/api/v1/predict")
async def predict(
    image: UploadFile = File(...),
    model_name: str = Form("Brain cancer model"),
):
    return {
        "study_id": "DEMO123",
        "classification": "Benign",
        "molecular_subtype": model_name,
        "confidence_metrics": {
            "primary_confidence": 0.91,
            "benign_probability": 0.91,
            "malignancy_probability": 0.09
        },
        "processing_time_ms": 1200,
        "recommendation": "Demo API is connected successfully. Now replace this with real model prediction.",
        "evidence": {
            "api_connection": 1
        },
        "predictions": [
            {
                "label": "Benign",
                "probability": 0.91
            },
            {
                "label": "Malignant",
                "probability": 0.09
            }
        ]
    }
