import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(page_title="Smart Crop Assistant", page_icon="🌾", layout="centered")

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
    <style>
        .stApp { background-color: #013220; color: #f0f0f0; }
        h1, h2, h3 { color: #f9f9f9; }
        .result-box {
            background: #024d1a;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        section[data-testid="stSidebar"] { background-color: #014d26; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# App Title
# ----------------------------
st.title("🌾 Smart Crop Assistant")
st.write("Predict yield & get farming recommendations based on soil, weather, NDVI, and crop history.")

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.header("🌱 Input Parameters")

farmer_name = st.sidebar.text_input("Farmer Name", "Tamlin")

soil_ph = st.sidebar.slider("Soil pH", 3.5, 9.0, 6.5)
nitrogen = st.sidebar.slider("Nitrogen (kg/ha)", 0, 200, 80)
phosphorus = st.sidebar.slider("Phosphorus (kg/ha)", 0, 100, 40)
potassium = st.sidebar.slider("Potassium (kg/ha)", 0, 100, 30)

rainfall = st.sidebar.slider("Rainfall (mm)", 0, 500, 150)
temperature = st.sidebar.slider("Temperature (°C)", 5, 45, 25)
humidity = st.sidebar.slider("Humidity (%)", 10, 100, 60)

ndvi = st.sidebar.slider("NDVI (0=poor, 1=excellent)", 0.0, 1.0, 0.6)

crop = st.sidebar.selectbox("Previous Crop", ["Wheat", "Rice", "Maize", "Soybean"])

# ----------------------------
# Dummy Logic
# ----------------------------
predicted_yield = (nitrogen * 0.05 + phosphorus * 0.03 + potassium * 0.04 +
                   (rainfall / 50) + (0.5 if 6 <= soil_ph <= 7.5 else -0.5) +
                   (ndvi * 5))

if rainfall < 100:
    irrigation = "Irrigation Needed 💧"
else:
    irrigation = "No Irrigation Required ✅"

fertilizer = []
if nitrogen < 50:
    fertilizer.append("Add Urea (Nitrogen)")
if phosphorus < 20:
    fertilizer.append("Add DAP (Phosphorus)")
if potassium < 20:
    fertilizer.append("Add MOP (Potassium)")
if not fertilizer:
    fertilizer.append("Soil nutrients are sufficient ✅")

if ndvi < 0.4 and humidity > 70:
    pest_alert = "⚠️ High risk of pest attack"
elif ndvi < 0.6:
    pest_alert = "⚠️ Moderate risk of pest attack"
else:
    pest_alert = "✅ Low pest risk"

# ----------------------------
# Display Results
# ----------------------------
st.markdown(f"<div class='result-box'><h3>👨‍🌾 Farmer: {farmer_name}</h3></div>", unsafe_allow_html=True)

st.markdown(f"<div class='result-box'><h3>📊 Predicted Yield</h3><p>{predicted_yield:.2f} tons/hectare</p></div>", unsafe_allow_html=True)

st.markdown(f"<div class='result-box'><h3>💧 Irrigation</h3><p>{irrigation}</p></div>", unsafe_allow_html=True)

st.markdown("<div class='result-box'><h3>🌿 Fertilizer Recommendation</h3>", unsafe_allow_html=True)
for f in fertilizer:
    st.markdown(f"<p>- {f}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<div class='result-box'><h3>🐛 Pest Alert</h3><p>{pest_alert}</p></div>", unsafe_allow_html=True)

# ----------------------------
# Charts Section
# ----------------------------
st.header("📈 Insights & Analysis")

# Line chart: Yield vs Rainfall
rainfall_range = np.linspace(0, 500, 20)
yield_simulation = [nitrogen * 0.05 + phosphorus * 0.03 + potassium * 0.04 +
                   (r / 50) + (ndvi * 5) for r in rainfall_range]

df_line = pd.DataFrame({"Rainfall (mm)": rainfall_range, "Predicted Yield": yield_simulation})
st.line_chart(df_line.set_index("Rainfall (mm)"))

# Bar chart: Nutrient comparison
nutrients = ["Nitrogen", "Phosphorus", "Potassium"]
current_levels = [nitrogen, phosphorus, potassium]
recommended_levels = [100, 50, 50]

df_bar = pd.DataFrame({
    "Nutrient": nutrients,
    "Current Level": current_levels,
    "Recommended Level": recommended_levels
})

st.bar_chart(df_bar.set_index("Nutrient"))

# ----------------------------
# Farmer's Yield History
# ----------------------------
st.header(f"📊 {farmer_name}'s Yield History")

# Dummy history for past 5 years
years = ["2019", "2020", "2021", "2022", "2023", "2024 (Predicted)"]
yields = [2.5, 3.0, 3.2, 2.8, 3.5, predicted_yield]

df_history = pd.DataFrame({"Year": years, "Yield (tons/ha)": yields})
st.bar_chart(df_history.set_index("Year"))
