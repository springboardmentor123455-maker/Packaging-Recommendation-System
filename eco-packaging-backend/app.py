from flask import Flask, jsonify, render_template, request
import mysql.connector

app = Flask(__name__)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="venky5678",
        database="eco_packaging_clean",
        port=3306
    )

# -----------------------------------
# UI ROUTE
# -----------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------------
# SYSTEM STATUS
# -----------------------------------
@app.route("/system-status")
def system_status():
    return jsonify({
        "engine": "Material Decision Engine",
        "status": "Running",
        "database": "eco_packaging_clean"
    })

# -----------------------------------
# DECISION ENGINE (NOT CALLED API)
# -----------------------------------
@app.route("/material-decision", methods=["POST"])
def material_decision():
    data = request.json or {}

    weight = data.get("weight", "Medium")
    fragility = data.get("fragility", "Medium")
    limit = int(data.get("limit", 100))

    weight_factor = {"Low": 5, "Medium": 0, "High": -5}
    fragility_factor = {"Low": 0, "Medium": -3, "High": -7}

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT material_type,
               biodegradability_score,
               recyclability_percent,
               co2_emission_score
        FROM materials
    """)

    materials = cursor.fetchall()
    cursor.close()
    conn.close()

    ranked = []

    for m in materials:
        base_score = (
            m["biodegradability_score"]
            + m["recyclability_percent"]
            - m["co2_emission_score"]
        )

        adjusted_score = (
            base_score
            + weight_factor.get(weight, 0)
            + fragility_factor.get(fragility, 0)
        )

        ranked.append({
            "material": m["material_type"],
            "score": adjusted_score
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return jsonify({
        "engine": "Material Decision Engine",
        "logic": "Multi-factor sustainability evaluation",
        "results": ranked[:limit]
    })

# -----------------------------------
# RUN SERVER
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
