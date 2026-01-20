from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf_report(filename, input_data, recommendations):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "EcoPackAI – Sustainability Recommendation Report")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    y -= 30

    # Product details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Product Details")
    y -= 20

    c.setFont("Helvetica", 10)
    for key, value in input_data.items():
        c.drawString(60, y, f"{key.replace('_',' ').title()}: {value}")
        y -= 15

    y -= 20

    # Recommendations table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Recommended Materials")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Material")
    c.drawString(180, y, "Cost/Kg")
    c.drawString(240, y, "CO₂")
    c.drawString(290, y, "Strength")
    c.drawString(350, y, "Score")
    y -= 15

    for item in recommendations:
        c.drawString(50, y, item["material_name"])
        c.drawString(180, y, str(item["cost_per_kg"]))
        c.drawString(240, y, str(item["co2_emission_score"]))
        c.drawString(290, y, str(item["strength_mpa"]))
        c.drawString(350, y, f"{item['material_score']:.3f}")
        y -= 15

        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
