import pandas as pd
import random

DATA_PATH = "../data/final_recommendations.csv"

def recommend_material(product_input):

    df = pd.read_csv(DATA_PATH)

    product = product_input.get("product_name", "").lower()
    weight = float(product_input.get("weight", 1))
    fragility = int(product_input.get("fragility", 3))

    # -----------------------------
    # PRODUCT CATEGORY LOGIC
    # -----------------------------
    if "food" in product:
        df = df[df["material_type"].isin(["Paper", "Natural"])]
        df = df[df["weight_g_per_m2"] <= 200]

    elif "electronics" in product:
        df = df[df["strength_kg"] >= 100]

    elif "glass" in product or fragility >= 4:
        df = df[df["strength_kg"] >= 130]

    # -----------------------------
    # WEIGHT SAFETY
    # -----------------------------
    df_safe = df[df["strength_kg"] >= weight * 15]
    if not df_safe.empty:
        df = df_safe

    # -----------------------------
    # AI SCORE
    # -----------------------------
    df["ai_score"] = (
        0.30 * df["biodegradability_score"] +
        0.25 * (1 - df["co2_emission_kg_per_kg"]) +
        0.20 * (df["recyclability_percent"] / 100) +
        0.15 * (1 / df["cost_kg"]) +
        0.10 * (df["strength_kg"] / 200)
    )

    # -----------------------------
    # FRAGILITY IMPACT
    # -----------------------------
    if fragility >= 4:
        df["ai_score"] += df["strength_kg"] * 0.015
    elif fragility <= 2:
        df["ai_score"] -= df["weight_g_per_m2"] * 0.002

    # -----------------------------
    # CONTROLLED RANDOMNESS (KEY!)
    # -----------------------------
    random.seed(product + str(weight) + str(fragility))
    df["ai_score"] += [random.uniform(-0.05, 0.05) for _ in range(len(df))]

    # -----------------------------
    # FINAL SORT
    # -----------------------------
    df = df.sort_values("ai_score", ascending=False)

    if df.empty:
        df = pd.read_csv(DATA_PATH).sample(5)

    return df.head(5)[[
        "material_name",
        "material_type",
        "strength_kg",
        "weight_g_per_m2",
        "ai_score"
    ]].to_dict(orient="records")
