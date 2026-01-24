from flask import Flask, jsonify, render_template, request, send_file
import psycopg2
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

app = Flask(__name__)

<<<<<<< HEAD
# ================= DATABASE =================
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_disabled=False
=======
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
>>>>>>> af1e87d85f9fc98d114bbbf046c236ae28c4ec07
    )

# ================= HOME =================
@app.route("/")
def index():
    return render_template("index.html")

<<<<<<< HEAD
# ================= RECOMMENDATION =================
@app.route("/material-decision", methods=["POST"])
def material_decision():
    try:
        data = request.get_json() or {}
        limit = int(data.get("limit", 10))
        category = data.get("category")
=======
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
>>>>>>> af1e87d85f9fc98d114bbbf046c236ae28c4ec07

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT material_type, biodegradability_score,
                   recyclability_percent, co2_emission_score
            FROM materials
            WHERE category = %s
        """, (category,))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

<<<<<<< HEAD
        ranked = []
        for r in rows:
            score = (
                r["biodegradability_score"]
                + r["recyclability_percent"]
                - r["co2_emission_score"]
            )
            ranked.append({
                "material_type": r["material_type"],
                "score": score,
                "co2_emission_score": r["co2_emission_score"],
                "recyclability_percent": r["recyclability_percent"]
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)
        ranked = ranked[:limit]
=======
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
>>>>>>> af1e87d85f9fc98d114bbbf046c236ae28c4ec07

        os.makedirs("reports", exist_ok=True)
        pd.DataFrame(ranked).to_csv("reports/last_recommendation.csv", index=False)

<<<<<<< HEAD
        return jsonify(ranked)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
=======
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
>>>>>>> af1e87d85f9fc98d114bbbf046c236ae28c4ec07

# ================= BI DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    path = "reports/last_recommendation.csv"
    os.makedirs("static", exist_ok=True)

    if not os.path.exists(path):
        return render_template("dashboard.html", co2_reduction=0, cost_savings=0)

    df = pd.read_csv(path)

    co2_reduction = round((1 - df["co2_emission_score"].mean() / 100) * 100, 2)
    cost_savings = round(df["recyclability_percent"].mean() * 10, 2)

    usage = df["material_type"].value_counts()

    plt.figure(figsize=(7,4))
    usage.plot(kind="bar", color="#16a085")
    plt.title("Recommended Material Usage")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("static/bar_chart.png")
    plt.close()

    plt.figure(figsize=(6,6))
    usage.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Recommendation Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("static/pie_chart.png")
    plt.close()

    return render_template(
        "dashboard.html",
        co2_reduction=co2_reduction,
        cost_savings=cost_savings
    )

<<<<<<< HEAD
# ================= EXCEL =================
@app.route("/download/excel")
def download_excel():
    path = "reports/last_recommendation.csv"
    df = pd.read_csv(path)
    out = "reports/sustainability_report.xlsx"
    df.to_excel(out, index=False)
    return send_file(out, as_attachment=True)
=======
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
>>>>>>> af1e87d85f9fc98d114bbbf046c236ae28c4ec07

# ================= PDF =================
@app.route("/download/pdf")
def download_pdf():
<<<<<<< HEAD
    df = pd.read_csv("reports/last_recommendation.csv")
    out = "reports/sustainability_report.pdf"

    c = canvas.Canvas(out, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Sustainability Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Eco-Friendly Packaging Recommendation System")
    y -= 20

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y, f"Generated on {datetime.now().strftime('%d %b %Y')}")
    y -= 30

    for _, row in df.iterrows():
        if y < 80:
            c.showPage()
            y = height - 50

        c.drawString(50, y, row["material_type"])
        c.drawString(260, y, str(row["co2_emission_score"]))
        c.drawString(350, y, str(row["recyclability_percent"]))
        y -= 15

    c.save()
    return send_file(out, as_attachment=True)

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
=======
    file_path = os.path.join(os.getcwd(), "reports", "sustainability_report.pdf")
    return send_file(file_path, as_attachment=True)

# -----------------------------------
# RUN SERVER (LOCAL ONLY)
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> af1e87d85f9fc98d114bbbf046c236ae28c4ec07
