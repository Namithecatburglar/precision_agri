import pandas as pd
import xgboost as xgb
import joblib
import os

# Load dataset
df = pd.read_csv("data/crop_yield.csv")

# Select features and target
features = ["Rainfall_mm", "Temperature_Celsius", "Fertilizer_Used", "Irrigation_Used", "Days_to_Harvest"]
target = "Yield_tons_per_ha"

X = df[features]
y = df[target]

# Train model
model = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1)
model.fit(X, y)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/crop_yield_model.pkl")

print("✅ Model trained and saved to model/crop_yield_model.pkl")
