import streamlit as st
from smart_crop_backend.utils import get_emotion
import pandas as pd
import numpy as np
import joblib
import os

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(page_title="Precision Agriculture", page_icon="🌾", layout="wide")

# ----------------------------
# Load Dataset & Model
# ----------------------------
csv_path = "data/crop_yield.csv"
df = pd.read_csv(csv_path) if os.path.exists(csv_path) else None

model_path = "model/crop_yield_model.pkl"
model = joblib.load(model_path) if os.path.exists(model_path) else None

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.title("🌱 Input Parameters")

farmer_name = st.sidebar.text_input("Farmer Name", "Tamlin")
crop_type = st.sidebar.selectbox("Crop Type", ["Wheat", "Rice", "Maize", "Soybean"])

rainfall = st.sidebar.slider("Rainfall (mm)", 0, 500, 150)
temperature = st.sidebar.slider("Temperature (°C)", 5, 45, 25)
days_to_harvest = st.sidebar.slider("Days to Harvest", 60, 180, 120)
fertilizer_used = st.sidebar.selectbox("Fertilizer Used", [0, 1])
irrigation_used = st.sidebar.selectbox("Irrigation Used", [0, 1])

st.sidebar.markdown("### 🧪 Soil & Pest Advisory")
nitrogen = st.sidebar.slider("Nitrogen (kg/ha)", 0, 200, 80)
phosphorus = st.sidebar.slider("Phosphorus (kg/ha)", 0, 100, 40)
potassium = st.sidebar.slider("Potassium (kg/ha)", 0, 100, 30)
soil_ph = st.sidebar.slider("Soil pH", 3.5, 9.0, 6.5)
humidity = st.sidebar.slider("Humidity (%)", 10, 100, 60)
ndvi = st.sidebar.slider("NDVI (0=poor, 1=excellent)", 0.0, 1.0, 0.6)

st.sidebar.title("🌱 Farmer Mood Check-In")
user_feeling = st.sidebar.text_input("How are you feeling today?")

if user_feeling:
    emotion, confidence = get_emotion(user_feeling)
    st.sidebar.markdown(f"**Detected Emotion:** `{emotion}` ({confidence})")

    # Optional motivational message
    if emotion == "anxious":
        st.sidebar.info("You're not alone. Let's look at your crop health and find a way forward.")
    elif emotion == "joy":
        st.sidebar.success("Great to hear! Let’s keep that momentum going.")
    elif emotion == "anger":
        st.sidebar.warning("Let’s channel that energy into smart decisions. We’ve got your back.")

# ----------------------------
# Prepare Input for Model
# ----------------------------
input_features = pd.DataFrame([{
    "Rainfall_mm": rainfall,
    "Temperature_Celsius": temperature,
    "Fertilizer_Used": fertilizer_used,
    "Irrigation_Used": irrigation_used,
    "Days_to_Harvest": days_to_harvest
}])

# ----------------------------
# Prediction
# ----------------------------
if model is not None:
    try:
        predicted_yield = model.predict(input_features)[0]
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
        predicted_yield = 0.0
else:
    st.error("❌ Model not loaded.")
    predicted_yield = 0.0

# ----------------------------
# Recommendations
# ----------------------------
def get_fertilizer_recommendation(n, p, k, ph):
    recs = []
    if n < 50: recs.append("🔴 Add Urea (Nitrogen) – 100 kg/ha")
    elif n < 80: recs.append("🟠 Top-up with Ammonium Sulphate – 50 kg/ha")
    if p < 20: recs.append("🔴 Add DAP (Phosphorus) – 60 kg/ha")
    elif p < 40: recs.append("🟠 Supplement with SSP – 40 kg/ha")
    if k < 20: recs.append("🔴 Add MOP (Potassium) – 50 kg/ha")
    elif k < 40: recs.append("🟠 Apply Potassium Nitrate – 30 kg/ha")
    if ph < 5.5: recs.append("🔴 Apply Lime – 1 ton/ha")
    elif ph > 8.0: recs.append("🟠 Apply Gypsum – 500 kg/ha")
    if not recs: recs.append("🟢 Soil nutrients are sufficient ✅")
    return recs

def get_pest_alert(ndvi, humidity):
    if ndvi < 0.4 and humidity > 70:
        return "🔴 High fungal risk. Apply fungicide immediately."
    elif ndvi < 0.6 and humidity > 60:
        return "🟠 Moderate aphid/mite risk. Monitor and apply neem-based spray."
    elif ndvi < 0.6 and humidity < 40:
        return "🟢 Low leafhopper risk. No action needed."
    else:
        return "✅ Pest risk minimal. Continue regular monitoring."

fertilizer_advice = get_fertilizer_recommendation(nitrogen, phosphorus, potassium, soil_ph)
pest_alert = get_pest_alert(ndvi, humidity)
irrigation_msg = "💧 Irrigation Needed" if rainfall < 100 else "✅ No Irrigation Required"

# ----------------------------
# Main Frame
# ----------------------------
st.title("🌾 Precision Agriculture")
st.markdown(f"Welcome, **{farmer_name}**! Here's your personalized crop dashboard.")

# ----------------------------
# Interactive Cards
# ----------------------------
card_option = st.selectbox("📊 Choose an insight to explore:", [
    "📉 Yield vs Rainfall",
    "🧪 Nutrient Comparison",
    f"📅 {farmer_name}'s Yield History"
])

if card_option == "📉 Yield vs Rainfall":
    st.subheader("📉 Yield vs Rainfall")
    rainfall_range = np.linspace(0, 500, 20)
    yield_simulation = []
    for r in rainfall_range:
        sim_input = pd.DataFrame([{
            "Rainfall_mm": r,
            "Temperature_Celsius": temperature,
            "Fertilizer_Used": fertilizer_used,
            "Irrigation_Used": irrigation_used,
            "Days_to_Harvest": days_to_harvest
        }])
        y = model.predict(sim_input)[0] if model else 0
        yield_simulation.append(y)
    df_line = pd.DataFrame({"Rainfall (mm)": rainfall_range, "Predicted Yield": yield_simulation})
    st.line_chart(df_line.set_index("Rainfall (mm)"))

elif card_option == "🧪 Nutrient Comparison":
    st.subheader("🧪 Nutrient Levels")
    df_bar = pd.DataFrame({
        "Nutrient": ["Nitrogen", "Phosphorus", "Potassium"],
        "Current Level": [nitrogen, phosphorus, potassium],
        "Recommended Level": [100, 50, 50]
    })
    st.bar_chart(df_bar.set_index("Nutrient"))

elif card_option == f"📅 {farmer_name}'s Yield History":
    st.subheader(f"📊 {farmer_name}'s Yield History")
    years = ["2019", "2020", "2021", "2022", "2023", "2024 (Predicted)"]
    yields = [2.5, 3.0, 3.2, 2.8, 3.5, predicted_yield]
    df_history = pd.DataFrame({"Year": years, "Yield (tons/ha)": yields})
    st.bar_chart(df_history.set_index("Year"))

# ----------------------------
# Prediction Results
# ----------------------------
st.subheader("🔍 Prediction & Recommendations")
st.metric("Predicted Yield", f"{predicted_yield:.2f} tons/ha")
st.success(irrigation_msg)
st.warning(pest_alert)

st.markdown("### 🌿 Fertilizer Recommendation")
for f in fertilizer_advice:
    st.markdown(f"- {f}")

# ----------------------------
# Season Details
# ----------------------------
if st.button("📅 Show Season Details"):
    input_2024 = pd.DataFrame([{
        "Rainfall_mm": rainfall,
        "Temperature_Celsius": temperature,
        "Fertilizer_Used": fertilizer_used,
        "Irrigation_Used": irrigation_used,
        "Days_to_Harvest": days_to_harvest
    }])
    yield_2024 = model.predict(input_2024)[0] if model else predicted_yield

    data_by_year = {
        "2019": {"nitrogen": 40, "phosphorus": 25, "potassium": 35, "rainfall": 950, "soil_ph": 6.2, "ndvi": 0.65, "yield": 2.5},
        "2022": {"nitrogen": 50, "phosphorus": 30, "potassium": 40, "rainfall": 1200, "soil_ph": 6.8, "ndvi": 0.75, "yield": 3.2},
        "2023": {"nitrogen": 45, "phosphorus": 28, "potassium": 38, "rainfall": 1100, "soil_ph": 6.5, "ndvi": 0.78, "yield": 3.5},
        "2024": {"nitrogen": nitrogen,"phosphorus": phosphorus,"potassium": potassium,"rainfall": rainfall,"soil_ph": soil_ph,"ndvi": ndvi,"yield": yield_2024}
    }

    def display_season_summary(year, stats):
        st.markdown(f"""
            <div style="
                background-color: #024d1a;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
                color: #f0f0f0;
            ">
                <h4>📅 {year} Season Summary</h4>
                <p>🌾 <b>Yield:</b> {stats.get('yield', 'N/A')} tons/ha</p>
                <p>🧪 <b>Nitrogen:</b> {stats.get('nitrogen', 'N/A')} kg/ha</p>
                <p>🧪 <b>Phosphorus:</b> {stats.get('phosphorus', 'N/A')} kg/ha</p>
                <p>🧪 <b>Potassium:</b> {stats.get('potassium', 'N/A')} kg/ha</p>
                <p>🌧️ <b>Rainfall:</b> {stats.get('rainfall', 'N/A')} mm</p>
                <p>🌡️ <b>Soil pH:</b> {stats.get('soil_ph', 'N/A')}</p>
                <p>🛰️ <b>NDVI:</b> {stats.get('ndvi', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

    selected_year = st.selectbox("Select a Year", list(data_by_year.keys()))
    stats = data_by_year.get(selected_year, {})
    display_season_summary(selected_year, stats)
