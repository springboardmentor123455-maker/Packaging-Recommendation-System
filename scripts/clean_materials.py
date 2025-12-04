# scripts/clean_materials.py
# Simple cleaning & feature creation for EcoPackAI materials dataset

import pandas as pd
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
data_dir = repo_root / "data"
infile = data_dir / "materials.csv"
outfile = data_dir / "materials_cleaned.csv"

print("Repo root:", repo_root)
print("Reading:", infile)

# Read
df = pd.read_csv(infile)

# Basic cleaning examples:
# 1. remove completely empty rows
df = df.dropna(how="all")

# 2. strip whitespace from string columns
for c in df.select_dtypes(include=["object"]).columns:
    df[c] = df[c].astype(str).str.strip()

# 3. fix numeric columns (coerce errors -> NaN)
num_cols = ["strength_kg", "weight_g_per_m2", "biodegradability_score", "co2_emission_kg_per_kg", "recyclability_percent", "unit_cost"]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# 4. fill missing numeric values with column median (safe default)
for c in num_cols:
    if c in df.columns:
        df[c].fillna(df[c].median(), inplace=True)

# 5. drop duplicates based on material_name if any
if "material_name" in df.columns:
    df = df.drop_duplicates(subset=["material_name"], keep="first").reset_index(drop=True)

# 6. Create example index score columns:
# CO2 Impact index (lower is better) normalized 0-1
if "co2_emission_kg_per_kg" in df.columns:
    df["co2_impact_index"] = (df["co2_emission_kg_per_kg"] - df["co2_emission_kg_per_kg"].min()) / (
        df["co2_emission_kg_per_kg"].max() - df["co2_emission_kg_per_kg"].min()
    )

# Recyclability normalized 0-1 (higher better)
if "recyclability_percent" in df.columns:
    df["recyclability_norm"] = df["recyclability_percent"] / 100.0

# Material suitability score (example: combine biodegradability & recyclability & inverse CO2)
# weights are example values
if all(c in df.columns for c in ["biodegradability_score", "recyclability_norm", "co2_impact_index"]):
    df["suitability_score"] = (
        0.45 * df["biodegradability_score"] + 0.35 * df["recyclability_norm"] + 0.20 * (1 - df["co2_impact_index"])
    )

# Save cleaned file
outfile.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(outfile, index=False)
print("Saved cleaned file:", outfile)
print("Rows:", len(df), "Columns:", len(df.columns))
