# scripts/data_cleaning.py
"""
Data cleaning and feature engineering for EcoPackAI (Module 2).
Produces: data/materials_cleaned.csv and writes to PostgreSQL table materials_cleaned.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_CSV = os.path.join(ROOT, "data", "materials_raw.csv")
CLEAN_CSV = os.path.join(ROOT, "data", "materials_cleaned.csv")

# Provide a PG_CONN via .env or edit here:
PG_CONN = os.getenv("PG_CONN", "postgresql+psycopg2://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/ecopackai_db")

def safe_minmax_scale(s: pd.Series):
    minv = s.min()
    maxv = s.max()
    if pd.isna(minv) or pd.isna(maxv) or maxv == minv:
        return pd.Series([0.0] * len(s), index=s.index)
    return (s - minv) / (maxv - minv)

def main():
    # 1. Read
    if not os.path.exists(RAW_CSV):
        print("ERROR: raw CSV not found at:", RAW_CSV)
        return

    df = pd.read_csv(RAW_CSV)
    print("Raw rows:", len(df))

    # 2. Basic cleaning
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype(str).str.strip()
    df = df.drop_duplicates().reset_index(drop=True)

    numeric_cols = ["strength_mpa", "weight_capacity_kg", "biodegradability_score",
                    "co2_emission_score", "recyclability_percent", "cost_per_kg"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in numeric_cols:
        if df[col].isnull().any():
            med = float(df[col].median(skipna=True))
            df[col] = df[col].fillna(med)
            print(f"Filled missing in {col} with median = {med}")

    # 3. Feature scaling
    df["scaled_strength"] = safe_minmax_scale(df["strength_mpa"])
    df["scaled_weight_capacity"] = safe_minmax_scale(df["weight_capacity_kg"])
    df["scaled_biodegradability"] = safe_minmax_scale(df["biodegradability_score"])
    df["scaled_co2"] = safe_minmax_scale(df["co2_emission_score"])
    df["scaled_recyclability"] = safe_minmax_scale(df["recyclability_percent"])
    df["scaled_cost"] = safe_minmax_scale(df["cost_per_kg"])

    # 4. Compute indices
    df["co2_impact_index"] = 0.6 * df["scaled_co2"] + 0.4 * (1.0 - df["scaled_biodegradability"])
    df["cost_efficiency_index"] = 0.7 * (1.0 - df["scaled_cost"]) + 0.3 * df["scaled_recyclability"]
    df["material_suitability_score"] = (
        0.25 * df["scaled_strength"]
        + 0.15 * df["scaled_weight_capacity"]
        + 0.35 * df["cost_efficiency_index"]
        + 0.25 * (1.0 - df["co2_impact_index"])
    )

    df = df.sort_values(by="material_suitability_score", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1

    keep_cols = [
        "rank", "material_name", "category",
        "strength_mpa", "weight_capacity_kg",
        "biodegradability_score", "co2_emission_score", "recyclability_percent", "cost_per_kg",
        "co2_impact_index", "cost_efficiency_index", "material_suitability_score",
        "scaled_strength", "scaled_weight_capacity", "scaled_biodegradability",
        "scaled_co2", "scaled_recyclability", "scaled_cost"
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    df_out = df[keep_cols].copy()

    df_out.to_csv(CLEAN_CSV, index=False)
    print("Saved cleaned CSV to:", CLEAN_CSV)

    # Write to Postgres if PG_CONN provided
    try:
        engine = create_engine(PG_CONN)
        df_out.to_sql("materials_cleaned", engine, if_exists="replace", index=False)
        print("Wrote cleaned table to Postgres: materials_cleaned")
    except Exception as e:
        print("Could not write to Postgres. Error:", e)
        print("Set PG_CONN in .env or update connection string in the script.")

if __name__ == "__main__":
    main()
