from flask import Flask, jsonify, render_template, request, send_file
import mysql.connector
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

app = Flask(__name__)

# ================= DATABASE =================
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_disabled=False
    )

# ================= HOME =================
@app.route("/")
def index():
    return render_template("index.html")

# ================= RECOMMENDATION =================
@app.route("/material-decision", methods=["POST"])
def material_decision():
    try:
        data = request.get_json() or {}
        limit = int(data.get("limit", 10))
        category = data.get("category")

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

        os.makedirs("reports", exist_ok=True)
        pd.DataFrame(ranked).to_csv("reports/last_recommendation.csv", index=False)

        return jsonify(ranked)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

# ================= EXCEL =================
@app.route("/download/excel")
def download_excel():
    path = "reports/last_recommendation.csv"
    df = pd.read_csv(path)
    out = "reports/sustainability_report.xlsx"
    df.to_excel(out, index=False)
    return send_file(out, as_attachment=True)

# ================= PDF =================
@app.route("/download/pdf")
def download_pdf():
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
