from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging

# ----------------------------
# App Setup
# ----------------------------
app = FastAPI(title="Smart Crop Yield Predictor 🌾")

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(level=logging.INFO)

# ----------------------------
# Load Model
# ----------------------------
try:
    model = joblib.load("crop_yield_model.pkl")
    logging.info("✅ Model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Failed to load model: {e}")
    model = None

# ----------------------------
# Input Schema
# ----------------------------
class InputData(BaseModel):
    rainfall: float
    temperature: float
    pesticide: float = 0.0  # Optional field with default

# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def health_check():
    return {"status": "Smart Crop API is running", "model_loaded": model is not None}

# ----------------------------
# Prediction Endpoint
# ----------------------------
@app.post("/predict")
def predict(data: InputData):
    if not model:
        return {"error": "Model not loaded"}

    input_df = pd.DataFrame([{
        "Rainfall": data.rainfall,
        "Temperature": data.temperature,
        "Pesticide": data.pesticide
    }])

    try:
        prediction = model.predict(input_df)[0]
        return {"predicted_yield": round(prediction, 2)}
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return {"error": f"Prediction failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)