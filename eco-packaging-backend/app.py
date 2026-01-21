from flask import Flask, jsonify, render_template, request, send_file
import psycopg2
import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# -----------------------------------
# DATABASE CONNECTION (POSTGRESQL)
# -----------------------------------
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", 5432)
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
        "database": os.environ.get("DB_NAME", "PostgreSQL")
    })

# -----------------------------------
# MATERIAL COMPARISON API
# -----------------------------------
@app.route("/material-comparison", methods=["POST"])
def material_comparison():
    data = request.json or {}

    weight = data.get("weight", "Medium")
    fragility = data.get("fragility", "Medium")
    limit = int(data.get("limit", 5))

    weight_factor = {"Low": 5, "Medium": 0, "High": -5}
    fragility_factor = {"Low": 0, "Medium": -3, "High": -7}

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT material_type,
               biodegradability_score,
               recyclability_percent,
               co2_emission_score
        FROM materials
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    comparison = []

    for r in rows:
        score = (
            r[1] + r[2] - r[3]
            + weight_factor.get(weight, 0)
            + fragility_factor.get(fragility, 0)
        )

        comparison.append({
            "material": r[0],
            "biodegradability": r[1],
            "recyclability": r[2],
            "co2_emission": r[3],
            "sustainability_score": score
        })

    comparison.sort(key=lambda x: x["sustainability_score"], reverse=True)
    return jsonify(comparison[:limit])

# -----------------------------------
# BI DASHBOARD ROUTE
# -----------------------------------
@app.route("/dashboard")
def dashboard():
    generate_charts()
    generate_excel()
    generate_pdf()

    return render_template(
        "dashboard.html",
        co2_reduction=35,
        cost_savings=18000,
        top_material="Bagasse"
    )

# -----------------------------------
# CHART GENERATION
# -----------------------------------
def generate_charts():
    os.makedirs("static/charts", exist_ok=True)

    materials = ["Bagasse", "Seaweed Wrap", "Mycelium", "Palm Leaf"]
    usage = [40, 25, 20, 15]

    plt.figure()
    plt.bar(materials, usage)
    plt.title("Material Usage Trends")
    plt.savefig("static/charts/material_usage.png")
    plt.close()

    plt.figure()
    plt.pie([65, 35], labels=["Reduced CO₂", "Remaining CO₂"], autopct="%1.1f%%")
    plt.title("CO₂ Reduction Analysis")
    plt.savefig("static/charts/co2_pie.png")
    plt.close()

# -----------------------------------
# EXCEL REPORT
# -----------------------------------
def generate_excel():
    REPORTS_DIR = os.path.join(os.getcwd(), "reports")
    os.makedirs(REPORTS_DIR, exist_ok=True)

    df = pd.DataFrame({
        "Metric": ["CO₂ Reduction (%)", "Cost Savings (₹)", "Top Material"],
        "Value": [35, 18000, "Bagasse"]
    })

    df.to_excel(os.path.join(REPORTS_DIR, "sustainability_report.xlsx"), index=False)

# -----------------------------------
# PDF REPORT
# -----------------------------------
def generate_pdf():
    REPORTS_DIR = os.path.join(os.getcwd(), "reports")
    os.makedirs(REPORTS_DIR, exist_ok=True)

    file_path = os.path.join(REPORTS_DIR, "sustainability_report.pdf")

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("Sustainability Report", styles["Title"]),
        Paragraph("CO₂ Reduction: 35%", styles["Normal"]),
        Paragraph("Cost Savings: ₹18,000", styles["Normal"]),
        Paragraph("Top Material: Bagasse", styles["Normal"])
    ]

    doc.build(content)

# -----------------------------------
# DOWNLOAD REPORTS
# -----------------------------------
@app.route("/download-excel")
def download_excel():
    file_path = os.path.join(os.getcwd(), "reports", "sustainability_report.xlsx")
    return send_file(file_path, as_attachment=True)

@app.route("/download-pdf")
def download_pdf():
    file_path = os.path.join(os.getcwd(), "reports", "sustainability_report.pdf")
    return send_file(file_path, as_attachment=True)

# -----------------------------------
# RUN SERVER (LOCAL ONLY)
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
