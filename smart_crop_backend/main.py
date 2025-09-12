from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load the pretrained model
try:
    model = joblib.load("crop_yield_model.pkl")
except:
    model = None

class InputData(BaseModel):
    rainfall: float
    temperature: float
    pesticide: float = 0.0  # Optional, default to 0.0

@app.post("/predict")
def predict(data: InputData):
    if model:
        input_df = pd.DataFrame([{
            "Rainfall": data.rainfall,
            "Temperature": data.temperature,
            "Pesticide": data.pesticide
        }])
        try:
            prediction = model.predict(input_df)[0]
            return {"predicted_yield": round(prediction, 2)}
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    else:
        return {"error": "Model not loaded"}
