from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load model
model_path = "model/crop_yield_model.pkl"
model = joblib.load(model_path) if os.path.exists(model_path) else None

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    fertilizer_advice = []
    pest_alert = ""
    irrigation_msg = ""
    farmer_name = "Tamlin"

    if request.method == "POST":
        farmer_name = request.form.get("farmer_name")
        crop_type = request.form.get("crop_type")
        rainfall = float(request.form.get("rainfall"))
        temperature = float(request.form.get("temperature"))
        days_to_harvest = int(request.form.get("days_to_harvest"))
        fertilizer_used = int(request.form.get("fertilizer_used"))
        irrigation_used = int(request.form.get("irrigation_used"))
        nitrogen = float(request.form.get("nitrogen"))
        phosphorus = float(request.form.get("phosphorus"))
        potassium = float(request.form.get("potassium"))
        soil_ph = float(request.form.get("soil_ph"))
        humidity = float(request.form.get("humidity"))
        ndvi = float(request.form.get("ndvi"))

        input_features = pd.DataFrame([{
            "Rainfall_mm": rainfall,
            "Temperature_Celsius": temperature,
            "Fertilizer_Used": fertilizer_used,
            "Irrigation_Used": irrigation_used,
            "Days_to_Harvest": days_to_harvest
        }])

        prediction = model.predict(input_features)[0] if model else 0.0

        # Fertilizer recommendation
        if nitrogen < 50: fertilizer_advice.append("🔴 Add Urea (Nitrogen) – 100 kg/ha")
        elif nitrogen < 80: fertilizer_advice.append("🟠 Top-up with Ammonium Sulphate – 50 kg/ha")
        if phosphorus < 20: fertilizer_advice.append("🔴 Add DAP (Phosphorus) – 60 kg/ha")
        elif phosphorus < 40: fertilizer_advice.append("🟠 Supplement with SSP – 40 kg/ha")
        if potassium < 20: fertilizer_advice.append("🔴 Add MOP (Potassium) – 50 kg/ha")
        elif potassium < 40: fertilizer_advice.append("🟠 Apply Potassium Nitrate – 30 kg/ha")
        if soil_ph < 5.5: fertilizer_advice.append("🔴 Apply Lime – 1 ton/ha")
        elif soil_ph > 8.0: fertilizer_advice.append("🟠 Apply Gypsum – 500 kg/ha")
        if not fertilizer_advice: fertilizer_advice.append("🟢 Soil nutrients are sufficient ✅")

        # Pest alert
        if ndvi < 0.4 and humidity > 70:
            pest_alert = "🔴 High fungal risk. Apply fungicide immediately."
        elif ndvi < 0.6 and humidity > 60:
            pest_alert = "🟠 Moderate aphid/mite risk. Monitor and apply neem-based spray."
        elif ndvi < 0.6 and humidity < 40:
            pest_alert = "🟢 Low leafhopper risk. No action needed."
        else:
            pest_alert = "✅ Pest risk minimal. Continue regular monitoring."

        irrigation_msg = "💧 Irrigation Needed" if rainfall < 100 else "✅ No Irrigation Required"

    return render_template("index.html",
                           prediction=prediction,
                           fertilizer_advice=fertilizer_advice,
                           pest_alert=pest_alert,
                           irrigation_msg=irrigation_msg,
                           farmer_name=farmer_name)

if __name__ == "__main__":
    app.run(debug=True)
