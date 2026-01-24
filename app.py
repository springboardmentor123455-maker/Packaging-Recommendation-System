from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import psycopg2
from flask import render_template


conn = psycopg2.connect(
    host="localhost",
    database="infosys",
    user="postgres",
    password="meeta"
)

cursor = conn.cursor()


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

    material = data["material"]   # ✅ MOVE THIS UP HERE

    row = {feature: 0 for feature in FEATURES}
    row["weight"] = data["weight"]
    row["durability"] = data["durability"]
    row["recyclable"] = data["recyclable"]

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

    if material in material_map:
        row[material_map[material]] = 1
    else:
        return jsonify({"error": "Invalid material"}), 400

    input_df = pd.DataFrame([row], columns=FEATURES)

    cost = float(cost_model.predict(input_df)[0])
    co2 = float(co2_model.predict(input_df)[0])

    env_score = calculate_environment_score(co2, data["recyclable"], data["durability"])

    # ✅ NOW database insert works
    cursor.execute("""
        INSERT INTO predictions 
        (weight, durability, recyclable, material, predicted_cost, predicted_co2, environment_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["weight"],
        data["durability"],
        data["recyclable"],
        material,
        cost,
        co2,
        env_score
    ))
    conn.commit()

    return jsonify({
        "predicted_cost": round(cost, 2),
        "predicted_co2": round(co2, 2),
        "environment_score": env_score
    })

@app.route("/recommend", methods=["POST"])
def recommend_material():
    data = request.get_json()

    materials = [
        {"name": "PLA Bioplastic", "co2": 1.2, "recyclable": 1, "durability": 8},
        {"name": "Recycled Paper", "co2": 0.8, "recyclable": 1, "durability": 5},
        {"name": "Plastic", "co2": 2.5, "recyclable": 0, "durability": 9}
    ]

    results = []
    for m in materials:
        score = calculate_environment_score(
            m["co2"],
            m["recyclable"],
            m["durability"]
        )
        results.append({
            "material": m["name"],
            "environment_score": score
        })

    best = max(results, key=lambda x: x["environment_score"])

    return jsonify({
        "recommended_material": best["material"],
        "ranking": sorted(results, key=lambda x: x["environment_score"], reverse=True)
    })

@app.route("/app")
def app_ui():
    return render_template("index.html")

# ✅ RUN SERVER (LAST LINE ONLY)
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)

