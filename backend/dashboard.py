from flask import jsonify, send_file
from pandas import ExcelWriter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
import os
from db import get_materials

# ---------------------------------
# PATH SETUP
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

PM_RANKING_NAMED = os.path.join(DATA_DIR, "product_material_ranking_named.csv")
PM_RANKING = os.path.join(DATA_DIR, "product_material_ranking.csv")
MATERIALS = os.path.join(DATA_DIR, "processed_materials.csv")
PRODUCTS = os.path.join(DATA_DIR, "processed_products.csv")

# ---------------------------------
# LOADERS
# ---------------------------------
def load_material_ranking():
    return pd.read_csv(PM_RANKING_NAMED)

def load_model_features():
    return pd.read_csv(PM_RANKING)

def load_materials():
    return pd.read_csv(MATERIALS)

def load_products():
    return pd.read_csv(PRODUCTS)

# ---------------------------------
# DASHBOARD METRICS (KPI)
# ---------------------------------
def dashboard_metrics():
    df = load_material_ranking()

    avg_score = round(df["Predicted_Suitability"].mean(), 3)

    top_row = df.sort_values(
        "Predicted_Suitability", ascending=False
    ).iloc[0]

    return jsonify({
        "avg_eco_score": avg_score,
        "top_recommended_material": top_row["material_name"],
        "top_material_score": round(top_row["Predicted_Suitability"], 3),
        "total_materials": len(df)
    })
def sustainability_kpis():
    materials = load_materials()

    avg_co2 = materials["CO2_Impact_Index"].mean()
    avg_cost = materials["Cost_Efficiency_Index"].mean()

    materials["co2_reduction_pct"] = (
        (avg_co2 - materials["CO2_Impact_Index"]) / avg_co2
    ) * 100

    materials["cost_savings_pct"] = (
        (materials["Cost_Efficiency_Index"] - avg_cost) / avg_cost
    ) * 100

    avg_co2 = materials["co2_reduction_pct"].mean()
    avg_cost = materials["cost_savings_pct"].mean()

# Clamp for dashboard readability
    avg_co2 = max(min(avg_co2, 100), -100)

    return jsonify({
    "avg_co2_reduction_pct": round(avg_co2, 2),
    "avg_cost_savings_pct": round(avg_cost, 2)
})

# ---------------------------------
# FULL MATERIAL IMPACT (ALL MATERIALS)
# ---------------------------------
def material_full_impact():
    materials = load_materials()

    output = materials[[
        "material_name",
        "CO2_Impact_Index",
        "Cost_Efficiency_Index"
    ]].rename(columns={
        "CO2_Impact_Index": "co2",
        "Cost_Efficiency_Index": "cost"
    })

    return jsonify(output.to_dict(orient="records"))


# ---------------------------------
# MATERIAL RANKING TREND (CHART)
# ---------------------------------
def material_trends():
    df = load_material_ranking()

    ranked = (
        df.sort_values("Predicted_Suitability", ascending=False)
          .reset_index(drop=True)
    )

    return jsonify(ranked.to_dict(orient="records"))



def material_impact_table():

    # Top 5 AI-ranked materials
    ranking = load_material_ranking().sort_values(
        "Predicted_Suitability", ascending=False
    ).head(5)

    # Processed material metrics (CO2 + cost)
    materials = load_materials()

    # Material names from PostgreSQL
    material_names = get_materials()

    output = []

    for i in range(min(5, len(material_names), len(materials))):
        output.append({
            "material_name": ranking.iloc[i]["material_name"],
            "eco_score": round(ranking.iloc[i]["Predicted_Suitability"], 3),
            "co2_index": round(materials.iloc[i]["CO2_Impact_Index"], 3),
            "cost_index": round(materials.iloc[i]["Cost_Efficiency_Index"], 3)
        })

    return jsonify(output)


# ---------------------------------
# FEATURE INFLUENCE 
# ---------------------------------
def feature_influence():
    df = load_model_features()

    corr = df.corr(numeric_only=True)["Predicted_Suitability"]
    corr = corr.drop("Predicted_Suitability")

    influence = (
        corr.sort_values(ascending=False)
            .reset_index()
            .rename(columns={
                "index": "feature",
                "Predicted_Suitability": "correlation"
            })
    )

    return jsonify(influence.to_dict(orient="records"))

# ---------------------------------
# EXPORT EXCEL
# ---------------------------------
def export_excel():
    path = os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.xlsx")

    ranking = pd.read_csv(PM_RANKING_NAMED)
    materials = pd.read_csv(MATERIALS)
    products = pd.read_csv(PRODUCTS)

    summary = pd.DataFrame([
        ["Average Eco Score", round(ranking["Predicted_Suitability"].mean(), 3)],
        ["Top Material",
         ranking.sort_values("Predicted_Suitability", ascending=False)
                .iloc[0]["material_name"]],
        ["CO₂ Reduction (%)",
         round(-ranking["Predicted_Suitability"].mean() * 100, 2)],
        ["Cost Savings (%)",
         round(ranking["Predicted_Suitability"].std() * 100, 2)]
    ], columns=["Metric", "Value"])

    with ExcelWriter(path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary_KPIs", index=False)
        ranking.to_excel(writer, sheet_name="Material_Ranking", index=False)
        materials.to_excel(writer, sheet_name="Material_Profile", index=False)
        products.to_excel(writer, sheet_name="Product_Profile", index=False)

    return send_file(
        path,
        as_attachment=True,
        download_name="EcoPack_Sustainability_Report.xlsx"
    )

# ---------------------------------
# EXPORT PDF (SUMMARY REPORT)
# ---------------------------------
def export_pdf():
    path = os.path.join(OUTPUT_DIR, "EcoPack_Sustainability_Report.pdf")

    ranking = pd.read_csv(PM_RANKING_NAMED)

    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(path, pagesize=A4)
    elements = []

    elements.append(
        Paragraph("<b>EcoPack AI – Sustainability Report</b>", styles["Title"])
    )
    elements.append(Spacer(1, 20))

    avg_score = round(ranking["Predicted_Suitability"].mean(), 3)
    top_material = ranking.sort_values(
        "Predicted_Suitability", ascending=False
    ).iloc[0]["material_name"]

    elements.append(Paragraph(
        f"""
        <b>Average Eco Score:</b> {avg_score}<br/>
        <b>Top Recommended Material:</b> {top_material}<br/>
        <b>CO₂ Reduction (Relative):</b> {-avg_score * 100:.2f}%<br/>
        <b>Cost Savings (Relative):</b>
        {ranking["Predicted_Suitability"].std() * 100:.2f}%
        """,
        styles["Normal"]
    ))

    elements.append(Spacer(1, 20))

    top5 = ranking.sort_values(
        "Predicted_Suitability", ascending=False
    ).head(5)

    table_data = [["Material", "Eco Suitability Score"]]
    for _, row in top5.iterrows():
        table_data.append([
            row["material_name"],
            round(row["Predicted_Suitability"], 3)
        ])

    table = Table(table_data, colWidths=[260, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    elements.append(table)
    report.build(elements)

    return send_file(
        path,
        as_attachment=True,
        download_name="EcoPack_Sustainability_Report.pdf"
    )

