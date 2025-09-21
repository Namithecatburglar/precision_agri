import pandas as pd
import xgboost as xgb
import joblib
import os

# ----------------------------
# Load Dataset
# ----------------------------
data_path = "data/crop_yield.csv"
df = pd.read_csv(data_path)

# ----------------------------
# Select Features & Target
# ----------------------------
features = [
    "Rainfall_mm",
    "Temperature_Celsius",
    "Fertilizer_Used",
    "Irrigation_Used",
    "Days_to_Harvest"
]
target = "Yield_tons_per_ha"

X = df[features]
y = df[target]

# ----------------------------
# Train Model
# ----------------------------
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    random_state=42
)
model.fit(X, y)

# ----------------------------
# Save Model
# ----------------------------
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/crop_yield_model.pkl")

print("✅ Model trained and saved to model/crop_yield_model.pkl")
