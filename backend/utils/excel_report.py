import pandas as pd
import os

def generate_excel_report(analytics, comparison, recommendations, output_path):
    """
    Generate sustainability report in Excel format
    """

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        # -------------------------
        # Sheet 1: Analytics Summary
        # -------------------------
        analytics_df = pd.DataFrame([analytics])
        analytics_df.to_excel(writer, sheet_name="Analytics Summary", index=False)

        # -------------------------
        # Sheet 2: Material Comparison
        # -------------------------
        comparison_df = pd.DataFrame([
            {"Type": "Baseline", **comparison["baseline"]},
            {"Type": "Recommended", **comparison["recommended"]}
        ])
        comparison_df.to_excel(writer, sheet_name="Material Comparison", index=False)

        # -------------------------
        # Sheet 3: Recommendations
        # -------------------------
        recommendations_df = pd.DataFrame(recommendations)
        recommendations_df.to_excel(writer, sheet_name="Top Recommendations", index=False)
