from flask import Flask, request, jsonify, send_from_directory
import pandas as pd

from model import (
    predict_cost,
    predict_co2,
    rank_materials_for_product
)

from db import get_materials, get_products
from auth import require_key
from dashboard import material_impact_table


from dashboard import (
    dashboard_metrics,
    material_trends,
    feature_influence,
    export_excel,
    export_pdf,
    sustainability_kpis
)

# -----------------------------------
# CREATE FLASK APP
# -----------------------------------
app = Flask(__name__, static_folder="static")

# -------------------------------
# BASIC LOOKUP APIs
# -------------------------------

@app.route("/materials")
@require_key
def materials():
    return jsonify(get_materials())

@app.route("/products")
@require_key
def products():
    return jsonify(get_products())

# -------------------------------
# GLOBAL ECO RANKING
# -------------------------------

@app.route("/global_rank")
@require_key
def global_rank():
    df = pd.read_csv(
        "D:/codingvscode/Python vscode/Packaging-Recommendation-System/data/material_ranking_named.csv"
    )

    top = df.sort_values("Rank").head(5)

    return jsonify(
        top[["material_name", "Final_Rank_Score", "Rank"]]
        .to_dict(orient="records")
    )

# -------------------------------
# PRODUCT-SPECIFIC MATERIAL RANKING
# -------------------------------

@app.route("/rank", methods=["POST"])
@require_key
def rank():
    data = request.json

    if not data or "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400

    product = data["product_name"]
    result = rank_materials_for_product(product)

    if result is None:
        return jsonify({"error": "Invalid product name"}), 400

    return jsonify(result)

# -------------------------------
# COST / CO2 / ECO SCORE
# -------------------------------

@app.route("/recommend", methods=["POST"])
@require_key
def recommend():
    data = request.json

    cost_cols = [
        "durability_score", "cushioning_score", "water_resistance_score",
        "weight_capacity_kg", "recyclability_score", "biodegradability_score",
        "Performance_Score", "Cost_Efficiency_Index", "CO2_Impact_Index", "inv_cost"
    ]

    X_cost = pd.DataFrame([[0] * len(cost_cols)], columns=cost_cols)

    for k in data:
        if k in X_cost.columns:
            X_cost.at[0, k] = float(data[k])

    cost = float(predict_cost(X_cost)[0])
    co2 = float(predict_co2(X_cost)[0])

    eco_score = round((1 / cost + 1 / co2), 3)

    return jsonify({
        "predicted_cost": cost,
        "predicted_co2": co2,
        "eco_score": eco_score
    })

# -------------------------------
# DASHBOARD (BI APIs)
# -------------------------------

@app.route("/dashboard/metrics")
@require_key
def metrics():
    return dashboard_metrics()


@app.route("/dashboard/material-trends")
@require_key
def material_usage():
    return material_trends()

@app.route("/dashboard/feature-influence")
@require_key
def feature_influence_api():
    return feature_influence()


@app.route("/dashboard/export/excel")
@require_key
def export_excel_api():
    return export_excel()

@app.route("/dashboard/export/pdf")
@require_key
def export_pdf_api():
    return export_pdf()

@app.route("/dashboard/sustainability-kpis")
@require_key
def sustainability_kpis_api():
    return sustainability_kpis()

@app.route("/dashboard/material-impact")
@require_key
def material_impact_api():
    return material_impact_table()

from dashboard import material_full_impact

@app.route("/dashboard/material-full-impact")
@require_key
def material_full_impact_api():
    return material_full_impact()

# -------------------------------
# FRONTEND
# -------------------------------

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# -------------------------------
# RUN SERVER
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
