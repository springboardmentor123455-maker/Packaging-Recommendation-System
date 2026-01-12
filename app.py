from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load models
cost_model = joblib.load("cost_model.pkl")
co2_model = joblib.load("co2_model.pkl")

# Helper function
def calculate_environment_score(co2, recyclable, durability):
    score = (1 / (1 + co2)) * 0.5 + recyclable * 0.3 + (durability / 10) * 0.2
    return round(score, 3)

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Eco Packaging AI Backend is running 🚀"})

FEATURES = [
    'weight',
    'durability',
    'recyclable',
    'material_Bagasse Fiber',
    'material_Biodegradable Plastic',
    'material_Corn Starch Polymer',
    'material_Glass',
    'material_Molded Pulp',
    'material_PLA Bioplastic',
    'material_Recycled Cardboard',
    'material_Recycled Paperboard'
]


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Create empty row with correct features
    row = {feature: 0 for feature in FEATURES}

    # Fill numeric values
    row["weight"] = data["weight"]
    row["durability"] = data["durability"]
    row["recyclable"] = data["recyclable"]

    # Handle material (ONE-HOT)
    material_map = {
        "Bagasse Fiber": "material_Bagasse Fiber",
        "Biodegradable Plastic": "material_Biodegradable Plastic",
        "Corn Starch Polymer": "material_Corn Starch Polymer",
        "Glass": "material_Glass",
        "Molded Pulp": "material_Molded Pulp",
        "PLA Bioplastic": "material_PLA Bioplastic",
        "Recycled Cardboard": "material_Recycled Cardboard",
        "Recycled Paperboard": "material_Recycled Paperboard"
    }

    material = data["material"]
    if material in material_map:
        row[material_map[material]] = 1
    else:
        return jsonify({"error": "Invalid material"}), 400

    # Create DataFrame in EXACT order
    input_df = pd.DataFrame([row], columns=FEATURES)

    # Predictions
    cost = float(cost_model.predict(input_df)[0])
    co2 = float(co2_model.predict(input_df)[0])

    env_score = calculate_environment_score(
        co2,
        data["recyclable"],
        data["durability"]
    )

    return jsonify({
        "predicted_cost": round(cost, 2),
        "predicted_co2": round(co2, 2),
        "environment_score": env_score
    })




# ✅ RUN SERVER (LAST LINE ONLY)
if __name__ == "__main__":
    app.run(debug=True)

