import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
import os

# ----------------------------
# Load Dataset
# ----------------------------
csv_path = "data/crop_yield.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError("❌ Dataset not found. Make sure 'crop_yield.csv' is inside the 'data/' folder.")

df = pd.read_csv(csv_path)
print("📋 Columns in dataset:", df.columns.tolist())
print("✅ Dataset loaded. Rows:", len(df))

# ----------------------------
# Preprocessing
# ----------------------------
# Drop rows with missing values
df = df.dropna()

# Select features and target
features = [
    "Rainfall_mm",
    "Temperature_Celsius",
    "Fertilizer_Used",       # Optional: include if numeric
    "Irrigation_Used",       # Optional: include if numeric
    "Days_to_Harvest"        # Optional: include if relevant
]

target = "Yield_tons_per_hectare"

X = df[features]
y = df[target]

# ----------------------------
# Train-Test Split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("✅ Data split into training and testing sets.")

# ----------------------------
# Train Model
# ----------------------------
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)
print("✅ Model training complete.")

# ----------------------------
# Evaluate Model
# ----------------------------
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Evaluation:")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.2f}")

# ----------------------------
# Save Model
# ----------------------------
model_path = "model/crop_yield_model.pkl"
joblib.dump(model, model_path)
print(f"\n✅ Model saved to: {model_path}")
