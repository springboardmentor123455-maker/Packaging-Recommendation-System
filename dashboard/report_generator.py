# report_generator.py
# Module 7: Sustainability Report Generator

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

print("\n==== SUSTAINABILITY REPORT GENERATOR ====\n")

# -------------------------------------------------
# Resolve base project directory safely
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
REPORTS_DIR = os.path.join(DASHBOARD_DIR, "reports")
DATA_FILE = os.path.join(REPORTS_DIR, "sustainability_data.csv")
EXCEL_FILE = os.path.join(REPORTS_DIR, "sustainability_report.xlsx")
PDF_FILE = os.path.join(REPORTS_DIR, "sustainability_report.pdf")

print(f"Base Directory: {BASE_DIR}")
print(f"Reports Directory: {REPORTS_DIR}")
print(f"Data File: {DATA_FILE}\n")


if not os.path.exists(DATA_FILE):
    raise FileNotFoundError("Run bi_dashboard.py first!")

data = pd.read_csv(DATA_FILE)
print("Sustainability Data Loaded Successfully\n")

# -------------------------------
# Export Excel Report
# -------------------------------
data.to_excel(EXCEL_FILE, index=False)

print("✔ Excel Report Generated")

# -------------------------------
# Export PDF Report
# -------------------------------
c = canvas.Canvas(PDF_FILE, pagesize=A4)
text = c.beginText(40, 800)

text.setFont("Helvetica-Bold", 14)
text.textLine("SUSTAINABILITY REPORT")
text.textLine("")

text.setFont("Helvetica", 10)
text.textLine("Material | CO₂ Reduction (%) | Cost Savings")
text.textLine("-------------------------------------------")

for _, row in data.iterrows():
    line = (
        f"{row['material']} | "
        f"{row['co2_reduction_percent']:.2f}% | "
        f"{row['cost_savings']}"
    )
    text.textLine(line)

c.drawText(text)
c.save()

print("✔ PDF Report Generated")
print("\nReport generation completed successfully!\n")
