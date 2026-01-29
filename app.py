from flask import send_file
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd
import psycopg2
import plotly.express as px
import pandas as pd
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

#Home route
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


@app.route("/dashboard")
def dashboard():
    df = pd.read_sql("SELECT * FROM predictions", conn)

    if df.empty:
        return "No prediction data available yet."

    # --- BUSINESS METRICS ---
    avg_co2 = df["predicted_co2"].mean()
    best_co2 = df["predicted_co2"].min()
    co2_reduction = round(((avg_co2 - best_co2) / avg_co2) * 100, 2)

    avg_cost = df["predicted_cost"].mean()
    min_cost = df["predicted_cost"].min()
    cost_savings = round(((avg_cost - min_cost) / avg_cost) * 100, 2)

    # --- CHARTS ---
    fig_co2 = px.line(df, x="created_at", y="predicted_co2",
                      title="CO₂ Emission Trend Over Time")

    fig_cost = px.line(df, x="created_at", y="predicted_cost",
                       title="Cost Prediction Trend")

    fig_material = px.histogram(df, x="material",
                                title="Material Usage Trends")

    fig_env = px.histogram(df, x="environment_score",
                           title="Environmental Score Distribution")

    return f"""
    <html>
    <head><title>EcoPackAI Dashboard</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>🌍 EcoPackAI Sustainability Dashboard</h1>

        <h2>📊 Key Sustainability Metrics</h2>
        <p><b>CO₂ Reduction Potential:</b> {co2_reduction}%</p>
        <p><b>Cost Savings Potential:</b> {cost_savings}%</p>

        <hr>
        {fig_co2.to_html(full_html=False)}
        {fig_cost.to_html(full_html=False)}
        {fig_material.to_html(full_html=False)}
        {fig_env.to_html(full_html=False)}

        <hr>
        <a href="/export/excel">⬇ Download Excel Report</a><br>
        <a href="/export/pdf">⬇ Download PDF Report</a>
    </body>
    </html>
    """


@app.route("/export/excel")
def export_excel():
    df = pd.read_sql("SELECT * FROM predictions", conn)

    if df.empty:
        return "No data available to export."

    # Sustainability metrics
    avg_co2 = df["predicted_co2"].mean()
    best_co2 = df["predicted_co2"].min()
    co2_reduction = round(((avg_co2 - best_co2) / avg_co2) * 100, 2)

    avg_cost = df["predicted_cost"].mean()
    min_cost = df["predicted_cost"].min()
    cost_savings = round(((avg_cost - min_cost) / avg_cost) * 100, 2)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Sheet 1: Raw predictions
        df.to_excel(writer, sheet_name="Predictions", index=False)

        # Sheet 2: Sustainability summary
        summary = pd.DataFrame({
            "Metric": ["CO₂ Reduction (%)", "Cost Savings (%)"],
            "Value": [co2_reduction, cost_savings]
        })
        summary.to_excel(writer, sheet_name="Sustainability Summary", index=False)

    output.seek(0)

    return send_file(
        output,
        download_name="EcoPackAI_Sustainability_Report.xlsx",
        as_attachment=True
    )



@app.route("/export/pdf")
def export_pdf():
    df = pd.read_sql("SELECT * FROM predictions", conn)

    if df.empty:
        return "No data available to export."

    avg_co2 = df["predicted_co2"].mean()
    best_co2 = df["predicted_co2"].min()
    co2_reduction = round(((avg_co2 - best_co2) / avg_co2) * 100, 2)

    avg_cost = df["predicted_cost"].mean()
    min_cost = df["predicted_cost"].min()
    cost_savings = round(((avg_cost - min_cost) / avg_cost) * 100, 2)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>EcoPackAI Sustainability Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"CO₂ Reduction Potential: {co2_reduction}%", styles["Normal"]))
    elements.append(Paragraph(f"Cost Savings Potential: {cost_savings}%", styles["Normal"]))
    elements.append(Spacer(1, 12))

    table_data = [["Material", "Predicted Cost", "Predicted CO₂", "Env Score"]]
    for _, row in df.iterrows():
        table_data.append([
            row["material"],
            round(row["predicted_cost"], 2),
            round(row["predicted_co2"], 2),
            round(row["environment_score"], 2)
        ])

    table = Table(table_data)
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        download_name="EcoPackAI_Sustainability_Report.pdf",
        as_attachment=True
    )
@app.route("/test")
def test():
    return "App is working!"



# ✅ RUN SERVER (LAST LINE ONLY)
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)


