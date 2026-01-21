import os
import pandas as pd
from sqlalchemy import text

# -------------------------
# Flask Imports
# -------------------------
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# -------------------------
# Project Imports
# -------------------------
from backend.db.database import engine
from backend.models.recommender import (
    get_material_recommendations,
    compute_business_metrics,
    compare_materials
)

from backend.utils.pdf_report import generate_pdf_report
from backend.utils.excel_report import generate_excel_report
from backend.utils.charts import (
    generate_comparison_charts,
    generate_usage_trend_chart
)

# -------------------------
# Base Directory
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------
# Flask App Setup
# -------------------------
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path=""
)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "EcoPackAI backend running"
    })

# -------------------------
# RECOMMENDATION API
# -------------------------
@app.route("/api/recommend", methods=["POST"])
def recommend_material():
    data = request.get_json()

    product_category = data.get("product_category")
    product_weight = data.get("product_weight")
    strength_required = data.get("strength_required")

    priority_strength = data.get("priority_strength", 3)
    priority_cost = data.get("priority_cost", 3)
    priority_co2 = data.get("priority_co2", 3)

    # ---- AI Recommendations ----
    recommendations = get_material_recommendations(
        product_category=product_category,
        product_weight=product_weight,
        strength_required=strength_required,
        priority_strength=priority_strength,
        priority_cost=priority_cost,
        priority_co2=priority_co2
    )

    # ---- Load baseline materials ----
    query = text("""
        SELECT cost_per_kg, co2_emission_score, strength_mpa
        FROM materials_cleaned
    """)
    all_materials_df = pd.read_sql(query, engine)

    # ---- Business Metrics ----
    analytics = compute_business_metrics(recommendations, all_materials_df)
    comparison = compare_materials(recommendations, all_materials_df)

    # ---- Charts ----
    charts_dir = os.path.join(app.root_path, "reports", "charts")
    os.makedirs(charts_dir, exist_ok=True)

    generate_comparison_charts(analytics, comparison, charts_dir)
    generate_usage_trend_chart(recommendations, charts_dir)

    return jsonify({
        "status": "success",
        "recommendations": recommendations,
        "analytics": analytics,
        "comparison": comparison,
        "charts": {
            "cost": "/charts/cost_comparison.png",
            "co2": "/charts/co2_comparison.png",
            "usage": "/charts/material_usage.png"
        }
    })

# -------------------------
# SERVE CHART IMAGES
# -------------------------
@app.route("/charts/<filename>")
def serve_charts(filename):
    charts_dir = os.path.join(app.root_path, "reports", "charts")
    return send_file(os.path.join(charts_dir, filename))

# -------------------------
# EXCEL EXPORT
# -------------------------
@app.route("/api/export/excel", methods=["POST"])
def export_excel():
    data = request.get_json()

    recommendations = get_material_recommendations(
        product_category=data.get("product_category"),
        product_weight=data.get("product_weight"),
        strength_required=data.get("strength_required"),
        priority_strength=data.get("priority_strength", 3),
        priority_cost=data.get("priority_cost", 3),
        priority_co2=data.get("priority_co2", 3)
    )

    query = text("""
        SELECT cost_per_kg, co2_emission_score, strength_mpa
        FROM materials_cleaned
    """)
    all_materials_df = pd.read_sql(query, engine)

    analytics = compute_business_metrics(recommendations, all_materials_df)
    comparison = compare_materials(recommendations, all_materials_df)

    report_dir = os.path.join(app.root_path, "reports")
    os.makedirs(report_dir, exist_ok=True)

    excel_path = os.path.join(report_dir, "EcoPackAI_Report.xlsx")

    generate_excel_report(
        analytics,
        comparison,
        recommendations,
        excel_path
    )

    return send_file(excel_path, as_attachment=True)

# -------------------------
# PDF EXPORT
# -------------------------
@app.route("/api/report", methods=["POST"])
def generate_report():
    data = request.get_json()

    recommendations = get_material_recommendations(
        product_category=data.get("product_category"),
        product_weight=data.get("product_weight"),
        strength_required=data.get("strength_required"),
        priority_strength=data.get("priority_strength", 3),
        priority_cost=data.get("priority_cost", 3),
        priority_co2=data.get("priority_co2", 3)
    )

    report_dir = os.path.join(app.root_path, "reports")
    os.makedirs(report_dir, exist_ok=True)

    report_path = os.path.join(report_dir, "EcoPackAI_Report.pdf")

    generate_pdf_report(report_path, data, recommendations)

    return send_file(report_path, as_attachment=True)

# -------------------------
# FRONTEND HOME
# -------------------------
@app.route("/")
def home():
    return app.send_static_file("index.html")

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

