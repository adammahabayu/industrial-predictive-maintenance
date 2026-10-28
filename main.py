from pathlib import Path
import json

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# ==========================================
# 1. KONFIGURASI DAN PEMUATAN MODEL
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "random_forest_rul_capped.joblib"
FEATURE_PATH = BASE_DIR / "feature_columns.json"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"File model tidak ditemukan: {MODEL_PATH}")

if not FEATURE_PATH.exists():
    raise FileNotFoundError(f"File fitur tidak ditemukan: {FEATURE_PATH}")

model = joblib.load(MODEL_PATH)

with open(FEATURE_PATH, "r", encoding="utf-8") as file:
    feature_columns = json.load(file)


# ==========================================
# 2. INISIALISASI FASTAPI
# ==========================================

app = FastAPI(
    title="Industrial Predictive Maintenance API",
    description=(
        "API untuk memperkirakan Remaining Useful Life (RUL) "
        "mesin menggunakan model Random Forest."
    ),
    version="1.0.0",
)


# ==========================================
# 3. SKEMA INPUT SENSOR
# ==========================================

class SensorInput(BaseModel):
    setting_1: float
    setting_2: float
    setting_3: float

    sensor_1: float
    sensor_2: float
    sensor_3: float
    sensor_4: float
    sensor_5: float
    sensor_6: float
    sensor_7: float
    sensor_8: float
    sensor_9: float
    sensor_10: float
    sensor_11: float
    sensor_12: float
    sensor_13: float
    sensor_14: float
    sensor_15: float
    sensor_16: float
    sensor_17: float
    sensor_18: float
    sensor_19: float
    sensor_20: float
    sensor_21: float


# ==========================================
# 4. ENDPOINT HEALTH CHECK
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Industrial Predictive Maintenance API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_type": type(model).__name__,
    }


# ==========================================
# 5. ENDPOINT PREDIKSI RUL
# ==========================================

@app.post("/predict")
def predict_rul(data: SensorInput):
    try:
        input_data = data.model_dump()

        input_df = pd.DataFrame(
            [input_data],
            columns=feature_columns,
        )

        prediction = float(model.predict(input_df)[0])

        # Model dilatih dengan label RUL capped maksimal 125.
        # Batasi output agar konsisten dengan definisi target model.
        prediction = max(0.0, min(prediction, 125.0))

        return {
            "predicted_rul": round(prediction, 2),
            "unit": "cycles",
            "interpretation": (
                "Perkiraan sisa siklus operasi berdasarkan model. "
                "Bukan jaminan umur mesin yang sebenarnya."
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediksi gagal: {str(exc)}",
        ) from exc