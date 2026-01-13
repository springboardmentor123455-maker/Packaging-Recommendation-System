import pandas as pd
import os

# Get absolute path of project root
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# Build dataset path safely
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_materials.csv")

#  LOAD DATASET (THIS WAS MISSING / NOT VISIBLE)
df = pd.read_csv(DATASET_PATH)


def recommend_material(weight, volume, fragility):
    # Calculate eco score
    df["eco_score"] = 100 - df["CO2_Emission_Score_kg"]

    # Use normalized cost for AI decision
    df_sorted = df.sort_values(
        by=["eco_score", "Cost_Efficiency_Index"],
        ascending=[False, True]
    )

    best = df_sorted.iloc[0]

    ranking = []
    for _, row in df_sorted.iterrows():
        ranking.append({
            "material": row["Material_ID"],
            "price_inr": round(row["Price_INR"], 2),
            "cost_index": round(row["Cost_Efficiency_Index"], 3),
            "co2": round(row["CO2_Emission_Score_kg"], 2),
            "eco_score": round(row["eco_score"], 2)
        })

    return {
        "best_material": best["Material_ID"],
        "best_price_inr": round(best["Price_INR"], 2),
        "best_cost_index": round(best["Cost_Efficiency_Index"], 3),
        "best_eco_score": round(best["eco_score"], 2),
        "ranking": ranking
    }
