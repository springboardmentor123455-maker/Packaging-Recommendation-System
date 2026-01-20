import pandas as pd
from sqlalchemy import text
from backend.db.database import engine

def get_material_recommendations(
    product_category,
    product_weight,
    strength_required,
    priority_strength,
    priority_cost,
    priority_co2
):
    """
    Category + user-priority aware recommendation logic
    """

    query = text("""
        SELECT material_name,
               strength_mpa,
               cost_per_kg,
               co2_emission_score,
               recyclability_percent
        FROM materials_cleaned
    """)

    df = pd.read_sql(query, engine)

    # Basic scores
    df["strength_score"] = df["strength_mpa"] / strength_required
    df["cost_score"] = 1 / df["cost_per_kg"]
    df["co2_score"] = 1 / df["co2_emission_score"]

    # Normalize user priorities
    total_priority = priority_strength + priority_cost + priority_co2

    w_strength = priority_strength / total_priority
    w_cost = priority_cost / total_priority
    w_co2 = priority_co2 / total_priority

    # Final weighted score
    df["material_score"] = (
        w_strength * df["strength_score"] +
        w_cost * df["cost_score"] +
        w_co2 * df["co2_score"]
    )

    df = df.sort_values("material_score", ascending=False)

    return df.head(5).to_dict(orient="records")
def compute_business_metrics(recommendations, all_materials_df):
    """
    Compute business analytics metrics for BI dashboard
    """

    # Baseline metrics (average of all materials)
    baseline_cost = all_materials_df["cost_per_kg"].mean()
    baseline_co2 = all_materials_df["co2_emission_score"].mean()

    # Best recommended material
    best_material = recommendations[0]

    cost_savings_pct = (
        (baseline_cost - best_material["cost_per_kg"]) / baseline_cost
    ) * 100

    co2_reduction_pct = (
        (baseline_co2 - best_material["co2_emission_score"]) / baseline_co2
    ) * 100

    return {
        "baseline_cost": round(baseline_cost, 2),
        "baseline_co2": round(baseline_co2, 2),
        "recommended_cost": best_material["cost_per_kg"],
        "recommended_co2": best_material["co2_emission_score"],
        "cost_savings_pct": round(cost_savings_pct, 2),
        "co2_reduction_pct": round(co2_reduction_pct, 2)
    }
def compare_materials(recommendations, all_materials_df):
    """
    Compare baseline material metrics with best recommended material
    """

    baseline = {
        "cost_per_kg": round(all_materials_df["cost_per_kg"].mean(), 2),
        "co2_emission_score": round(all_materials_df["co2_emission_score"].mean(), 2),
        "strength_mpa": round(all_materials_df["strength_mpa"].mean(), 2)
    }

    best = recommendations[0]

    return {
        "baseline": baseline,
        "recommended": {
            "material_name": best["material_name"],
            "cost_per_kg": best["cost_per_kg"],
            "co2_emission_score": best["co2_emission_score"],
            "strength_mpa": best["strength_mpa"],
            "material_score": round(best["material_score"], 3)
        }
    }

