import os
import matplotlib
matplotlib.use("Agg")  # IMPORTANT for Render (no GUI)
import matplotlib.pyplot as plt


def generate_comparison_charts(analytics, comparison, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Cost comparison
    plt.figure()
    plt.bar(
        ["Baseline", "Recommended"],
        [comparison["baseline"]["cost_per_kg"], comparison["best"]["cost_per_kg"]],
    )
    plt.title("Cost Comparison")
    plt.ylabel("Cost per Kg")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "cost_comparison.png"))
    plt.close()

    # CO2 comparison
    plt.figure()
    plt.bar(
        ["Baseline", "Recommended"],
        [
            comparison["baseline"]["co2_emission_score"],
            comparison["best"]["co2_emission_score"],
        ],
    )
    plt.title("CO₂ Emission Comparison")
    plt.ylabel("CO₂ Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "co2_comparison.png"))
    plt.close()


def generate_usage_trend_chart(recommendations, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    materials = [r["material_name"] for r in recommendations]
    scores = [r["material_score"] for r in recommendations]

    plt.figure(figsize=(8, 4))
    plt.bar(materials, scores)
    plt.xticks(rotation=30, ha="right")
    plt.title("Material Usage Trend")
    plt.ylabel("Material Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "material_usage.png"))
    plt.close()
