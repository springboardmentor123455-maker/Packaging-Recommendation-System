from flask import jsonify, send_file
import pandas as pd
import numpy as np
import os
import joblib

from pandas import ExcelWriter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from model import rank_materials_for_product, predict_cost, predict_co2
import pandas as pd
from model import rank_materials_for_product

# =================================================
# PATHS
# =================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR   = os.path.join(BASE_DIR, "data")
MODEL_DIR  = os.path.join(BASE_DIR, "trained_models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

RAW_MATERIALS = os.path.join(DATA_DIR, "materials.csv")
PROCESSED_MATERIALS = os.path.join(DATA_DIR, "processed_materials.csv")

GLOBAL_RANKING = os.path.join(DATA_DIR, "material_ranking_named.csv")
PRODUCT_RANKING = os.path.join(DATA_DIR, "product_material_ranking_named.csv")

RAW_MATERIALS = os.path.join(DATA_DIR, "materials.csv")
RAW_PRODUCTS  = os.path.join(DATA_DIR, "products.csv")
# =================================================
# LOAD MODELS
# =================================================

COST_MODEL = joblib.load(os.path.join(MODEL_DIR, "cost_model.pkl"))
CO2_MODEL  = joblib.load(os.path.join(MODEL_DIR, "co2_model.pkl"))

USD_TO_INR = 83

# =================================================
# LOADERS
# =================================================

def load_materials():
    return pd.read_csv(PROCESSED_MATERIALS)

def load_global_ranking():
    return pd.read_csv(GLOBAL_RANKING)

def load_raw_material_names():
    return pd.read_csv(RAW_MATERIALS)

def load_raw_product_names():
    return pd.read_csv(RAW_PRODUCTS)



def build_material_features(row):
    # Get exact training feature order from model
    feature_order = COST_MODEL.feature_names_in_

    data = {}

    for feature in feature_order:
        if feature == "inv_cost":
            data["inv_cost"] = (
                1 / row["cost_per_kg"] if row["cost_per_kg"] != 0 else 0
            )
        else:
            data[feature] = row[feature]

    return pd.DataFrame([data], columns=feature_order)


# =================================================
# DASHBOARD METRICS
# =================================================
def dashboard_metrics():
    ranking = load_global_ranking()

    avg_score = round(ranking["Final_Rank_Score"].mean(), 3)

    top_row = ranking.sort_values("Rank").iloc[0]

    return jsonify({
        "avg_eco_score": avg_score,
        "top_recommended_material": top_row["material_name"],
        "top_material_score": round(top_row["Final_Rank_Score"], 3),
        "total_materials": len(ranking)
    })


# =================================================
# SUSTAINABILITY KPIs
# =================================================

def sustainability_kpis():
    df = load_materials()

    def normalize(series):
        return (series - series.min()) / (series.max() - series.min())

    # Normalize indexes
    co2_norm = normalize(df["CO2_Impact_Index"])
    cost_norm = normalize(df["Cost_Efficiency_Index"])

    # Lower CO2 index = better
    avg_co2_reduction = round((1 - co2_norm.mean()) * 100, 1)

    # Higher cost efficiency = better
    avg_cost_savings = round(cost_norm.mean() * 100, 1)

    return jsonify({
        "avg_co2_reduction_pct": avg_co2_reduction,
        "avg_cost_savings_pct": avg_cost_savings
    })


# =================================================
# GLOBAL TOP 5 MATERIALS
# =================================================
def global_material_table():
    df = load_global_ranking().sort_values("Rank")

    output = []

    for _, r in df.head(5).iterrows():
        output.append({
            "material_name": r["material_name"],
            "eco_rank": int(r["Rank"]),
            "co2_score": round(abs(r["Predicted_CO2_Index"]), 3),
            "estimated_cost": round(abs(r["Predicted_Cost_Index"]) * 100, 2)
        })

    return jsonify(output)

# =================================================
# PRODUCT MATERIAL TABLE
# =================================================

def product_material_table(product=None):

    if not product:
        return jsonify([])

    # 🔥 product-specific ML ranking
    ranking = rank_materials_for_product(product)

    materials = pd.read_csv(PROCESSED_MATERIALS)
    raw_materials = pd.read_csv(os.path.join(DATA_DIR, "materials.csv"))

    output = []

    for r in ranking:

        mat_name = r["material_name"]

        # 🔥 find material index from raw materials
        match = raw_materials[raw_materials["material_name"] == mat_name]

        if match.empty:
            continue

        mat_idx = match.index[0]

        row = materials.iloc[mat_idx]

        # build ML features
        X = build_material_features(row)

        cost = float(predict_cost(X)[0])
        co2  = float(predict_co2(X)[0])

        # normalize suitability (human readable)
        suitability_score = round((r["Predicted_Suitability"] + 1) * 50, 1)

        output.append({
            "material_name": mat_name,
            "Predicted_Suitability": suitability_score,
            "co2_score": round(abs(co2), 3),
            "estimated_cost": f"₹{round(abs(cost) * 100, 2)}"
        })

    return jsonify(output)

# =================================================
# MATERIAL TRENDS
# =================================================
def material_trends():
    ranking = pd.read_csv(GLOBAL_RANKING)
    raw = load_raw_material_names()

    # attach real names
    ranking["material_name"] = raw["material_name"]

    ranking = ranking.sort_values("Rank")

    return jsonify(ranking[[
        "material_name",
        "Final_Rank_Score",
        "Rank"
    ]].to_dict(orient="records"))


# =================================================
# FULL MATERIAL IMPACT
# =================================================

def material_full_impact():
    materials = pd.read_csv(PROCESSED_MATERIALS)
    raw = load_raw_material_names()

    materials["material_name"] = raw["material_name"]

    return jsonify(
        materials[[
            "material_name",
            "CO2_Impact_Index",
            "Cost_Efficiency_Index"
        ]]
        .rename(columns={
            "CO2_Impact_Index": "co2",
            "Cost_Efficiency_Index": "cost"
        })
        .to_dict(orient="records")
    )


# =================================================
# FEATURE INFLUENCE
# =================================================

def feature_influence():
    df = load_materials()

    corr = df.corr(numeric_only=True)["Material_Suitability_Score"]
    corr = corr.drop("Material_Suitability_Score")

    influence = (
        corr.sort_values(ascending=False)
        .reset_index()
        .rename(columns={
            "index": "feature",
            "Material_Suitability_Score": "correlation"
        })
    )

    return jsonify(influence.to_dict(orient="records"))

def export_excel(product=None):

    if not product:
        product = "Selected Product"

    ranking = rank_materials_for_product(product)

    rows = []

    for r in ranking:
        rows.append({
            "Material": r["material_name"],
            "Suitability (0–100)": round(r["Predicted_Suitability"], 1),
        
        })

    df = pd.DataFrame(rows)

    path = os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.xlsx")

    with ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Product Recommendations", index=False)

    return send_file(
        path,
        as_attachment=True,
        download_name="EcoPack_Sustainability_Report.xlsx"
    )



def export_pdf(product=None):

    if not product:
        product = "Selected Product"

    # 🔥 REAL ML — SAME AS UI
    ranking = rank_materials_for_product(product)

    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.pdf"),
        pagesize=A4
    )

    elements = []

    elements.append(
        Paragraph("EcoPack AI – Sustainability Report", styles["Title"])
    )

    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph(f"<b>Selected Product:</b> {product}", styles["Normal"])
    )

    elements.append(Spacer(1, 20))

    table_data = [
        ["Material", "Suitability", "Estimated CO₂", "Estimated Cost (₹)"]
    ]

    for r in ranking:
        table_data.append([
            r["material_name"],
            round(r["Predicted_Suitability"], 1),
            r.get("co2_score", "-"),
            r.get("estimated_cost", "-")
        ])

    table = Table(table_data, colWidths=[170, 90, 90, 110])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    elements.append(table)

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph("<b>Interpretation Guide</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            """
            • Suitability Score: Relative ML-based indicator (0–100) showing how appropriate
            a material is for the selected product.<br/>
            • Estimated CO₂: Relative environmental impact predicted by AI model.
            Lower values indicate lower emissions.<br/>
            • Estimated Cost: Relative production cost prediction in Indian Rupees.<br/>
            • Product Ranking: Product-aware recommendation generated using trained ML models.
            """,
            styles["Normal"]
        )
    )

    report.build(elements)

    return send_file(
        os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.pdf"),
        as_attachment=True,
        download_name="EcoPack_Sustainability_Report.pdf"
    )
def export_pdf(product=None):

    if not product:
        product = "Selected Product"

    ranking = rank_materials_for_product(product)

    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.pdf"),
        pagesize=A4
    )

    elements = []

    # ----------------------------
    # TITLE
    # ----------------------------
    elements.append(
        Paragraph("EcoPack AI – Sustainability Report", styles["Title"])
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"<b>Selected Product:</b> {product}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ----------------------------
    # TABLE
    # ----------------------------
    table_data = [
        ["Material", "Sustainability Score (0–100)"]
    ]

    for r in ranking:
        table_data.append([
            r["material_name"],
            round(r["Predicted_Suitability"], 1)
        ])

    table = Table(table_data, colWidths=[260, 180])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 25))

    # ----------------------------
    # INTERPRETATION GUIDE
    # ----------------------------
    elements.append(
        Paragraph("Interpretation Guide", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            """
            • Sustainability Score (0–100): Relative AI-based indicator showing how suitable
            a packaging material is for the selected product.<br/>
            • Scores are derived from trained machine learning models and should be interpreted
            comparatively rather than as absolute environmental measurements.<br/>
            • Higher scores indicate better overall sustainability suitability for the product.
            """,
            styles["Normal"]
        )
    )

    report.build(elements)

    return send_file(
        os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.pdf"),
        as_attachment=True,
        download_name="EcoPack_Sustainability_Report.pdf"
    )
