import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet

# ---------------------------------------------------
# CONFIG (same backend as Module 6)
# ---------------------------------------------------
BASE_URL = "http://127.0.0.1:5000"
API_KEY = "super"   # same X-API-Key used earlier
HEADERS = {"X-API-Key": API_KEY}

# ---------------------------------------------------
# FETCH DATA FROM MODULE 5 API
# ---------------------------------------------------
materials_res = requests.get(f"{BASE_URL}/api/materials", headers=HEADERS)
materials = materials_res.json()["data"]["materials"]

if not materials:
    raise RuntimeError("No materials found. Add materials using Module 6 UI.")

df = pd.DataFrame(materials)

# ---------------------------------------------------
# BUSINESS INTELLIGENCE CALCULATIONS
# ---------------------------------------------------

# Assume baseline values (for academic/demo purpose)
BASELINE_COST = 200
BASELINE_CO2 = 20

df["co2_reduction_pct"] = (
    (BASELINE_CO2 - df["predicted_co2_kgCO2_per_kg"]) / BASELINE_CO2
) * 100

df["cost_savings"] = BASELINE_COST - df["predicted_cost_per_kg_usd"]

df["usage_count"] = range(1, len(df) + 1)

# ---------------------------------------------------
# MATPLOTLIB DASHBOARD
# ---------------------------------------------------

# CO2 Reduction
plt.figure()
plt.bar(df["name"], df["co2_reduction_pct"])
plt.title("CO₂ Reduction Percentage by Material")
plt.ylabel("Reduction (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("co2_reduction.png")
plt.show()

# Cost Savings
plt.figure()
plt.bar(df["name"], df["cost_savings"])
plt.title("Cost Savings by Material")
plt.ylabel("Savings (USD/kg)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cost_savings.png")
plt.show()

# ---------------------------------------------------
# PLOTLY INTERACTIVE TREND
# ---------------------------------------------------
fig = px.line(
    df,
    x="name",
    y="usage_count",
    title="Material Usage Trends"
)
fig.show()

# ---------------------------------------------------
# EXPORT TO EXCEL
# ---------------------------------------------------
excel_file = "sustainability_report.xlsx"
df.to_excel(excel_file, index=False)

# ---------------------------------------------------
# EXPORT TO PDF
# ---------------------------------------------------
pdf_file = "sustainability_report.pdf"
doc = SimpleDocTemplate(pdf_file)
styles = getSampleStyleSheet()
elements = []

elements.append(Paragraph("EcoPackAI – Sustainability Report", styles["Title"]))
elements.append(Paragraph("Module 7: Business Intelligence Dashboard", styles["Heading2"]))

table_data = [df.columns.tolist()] + df.values.tolist()
table = Table(table_data)
elements.append(table)

doc.build(elements)

print("✅ Module 7 Dashboard & Reports Generated Successfully")
