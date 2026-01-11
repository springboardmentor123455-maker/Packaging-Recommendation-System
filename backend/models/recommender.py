import pandas as pd
import numpy as np
from sqlalchemy import text
from backend.db.database import engine

def get_material_recommendations(product_weight, strength_required):
    """
    Simple AI-based recommendation using rule + score logic
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

    # Suitability checks
    df["strength_score"] = df["strength_mpa"] / strength_required
    df["weight_score"] = 1 / product_weight

    # Composite ranking score
    df["material_score"] = (
        0.4 * df["strength_score"] +
        0.3 * (1 / df["cost_per_kg"]) +
        0.3 * (1 / df["co2_emission_score"])
    )

    df = df.sort_values("material_score", ascending=False)

    return df.head(5).to_dict(orient="records")