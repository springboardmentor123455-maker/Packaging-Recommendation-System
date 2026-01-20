import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use("Agg")
Flask==3.1.2
flask-cors==6.0.2
gunicorn==23.0.0

pandas==2.3.3
numpy==2.3.5
sqlalchemy==2.0.45
psycopg2-binary==2.9.11

matplotlib==3.10.8
openpyxl==3.1.5
reportlab==4.2.5
python-dotenv==1.2.1



def generate_comparison_charts(analytics, comparison, output_dir):
    """
    Generates cost & CO2 comparison charts
    """

    os.makedirs(output_dir, exist_ok=True)

    # -------------------------
    # COST COMPARISON CHART
    # -------------------------
    plt.figure()
    plt.bar(
        ["Baseline Cost", "Recommended Cost"],
        [analytics["baseline_cost"], analytics["recommended_cost"]]
    )
    plt.title("Cost Comparison")
    plt.ylabel("Cost per Kg")
    plt.savefig(os.path.join(output_dir, "cost_comparison.png"))
    plt.close()

    # -------------------------
    # CO2 COMPARISON CHART
    # -------------------------
    plt.figure()
    plt.bar(
        ["Baseline CO₂", "Recommended CO₂"],
        [analytics["baseline_co2"], analytics["recommended_co2"]]
    )
    plt.title("CO₂ Emission Comparison")
    plt.ylabel("CO₂ Score")
    plt.savefig(os.path.join(output_dir, "co2_comparison.png"))
    plt.close()


def generate_usage_trend_chart(recommendations, output_dir):
    """
    Generates material usage trend chart
    """

    os.makedirs(output_dir, exist_ok=True)

    material_names = [r["material_name"] for r in recommendations]
    counts = {}

    for name in material_names:
        counts[name] = counts.get(name, 0) + 1

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title("Material Usage Trend")
    plt.ylabel("Frequency")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "material_usage.png"))
    plt.close()
