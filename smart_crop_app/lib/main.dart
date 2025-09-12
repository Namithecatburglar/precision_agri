import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(SmartCropApp());

class SmartCropApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Crop Assistant',
      theme: ThemeData.dark(),
      home: CropForm(),
    );
  }
}

class CropForm extends StatefulWidget {
  @override
  _CropFormState createState() => _CropFormState();
}

class _CropFormState extends State<CropForm> {
  double nitrogen = 80, phosphorus = 40, potassium = 30, rainfall = 150, soilPh = 6.5, ndvi = 0.6;
  String result = "";

  Future<void> getPrediction() async {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/predict'), // Use 10.0.2.2 for Android emulator
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "rainfall": rainfall,
        "soil_ph": soilPh,
        "ndvi": ndvi
      }),
    );

    final data = jsonDecode(response.body);
    setState(() {
      result = "🌾 Predicted Yield: ${data['predicted_yield']} tons/ha";
    });
  }

  Widget buildSlider(String label, double value, double min, double max, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text("$label: ${value.toStringAsFixed(1)}", style: TextStyle(fontSize: 16)),
        Slider(value: value, min: min, max: max, onChanged: onChanged),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Smart Crop Assistant')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            buildSlider("Nitrogen", nitrogen, 0, 200, (val) => setState(() => nitrogen = val)),
            buildSlider("Phosphorus", phosphorus, 0, 100, (val) => setState(() => phosphorus = val)),
            buildSlider("Potassium", potassium, 0, 100, (val) => setState(() => potassium = val)),
            buildSlider("Rainfall", rainfall, 0, 500, (val) => setState(() => rainfall = val)),
            buildSlider("Soil pH", soilPh, 3.5, 9.0, (val) => setState(() => soilPh = val)),
            buildSlider("NDVI", ndvi, 0.0, 1.0, (val) => setState(() => ndvi = val)),
            SizedBox(height: 20),
            ElevatedButton(onPressed: getPrediction, child: Text("Predict Yield")),
            SizedBox(height: 20),
            Text(result, style: TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
