import pandas as pd

def generate_excel_report(analytics, comparison, recommendations, output_path):
    """
    Generate Excel report with analytics, comparison, and recommendations.
    """

    # ---- Sheet 1: Analytics ----
    analytics_df = pd.DataFrame([analytics])

    # ---- Sheet 2: Comparison ----
    comparison_df = pd.DataFrame([
        {"Type": "Baseline", **comparison["baseline"]},
        {"Type": "Best Recommended", **comparison["best"]}
    ])

    # ---- Sheet 3: Recommendations ----
    recommendations_df = pd.DataFrame(recommendations)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        analytics_df.to_excel(writer, sheet_name="Analytics", index=False)
        comparison_df.to_excel(writer, sheet_name="Comparison", index=False)
        recommendations_df.to_excel(writer, sheet_name="Recommendations", index=False)
