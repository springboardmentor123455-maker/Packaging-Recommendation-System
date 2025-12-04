import pandas as pd
import numpy as np

df = pd.read_csv("data/materials.csv")

# Clean columns
df.columns = [c.strip() for c in df.columns]

num_cols = ['strength_kg','weight_g_per_m2','biodegradability_score',
            'co2_emission_kg_per_kg','recyclability_percent','unit_cost']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

df[num_cols] = df[num_cols].fillna(df[num_cols].median())

df['material_type'] = df['material_type'].astype('category')

# CO2 Impact Index
minv = df['co2_emission_kg_per_kg'].min()
maxv = df['co2_emission_kg_per_kg'].max()
df['co2_impact_index'] = (df['co2_emission_kg_per_kg'] - minv) / (maxv - minv + 1e-9)

# Cost Index
minc = df['unit_cost'].min()
maxc = df['unit_cost'].max()
df['cost_index'] = 1 - ((df['unit_cost'] - minc) / (maxc - minc + 1e-9))

# Suitability Score
df['material_suitability'] = (
    0.35 * df['biodegradability_score'] +
    0.25 * (df['recyclability_percent'] / 100) -
    0.20 * df['co2_impact_index'] +
    0.20 * df['cost_index']
)

df.to_csv("data/materials_cleaned.csv", index=False)
print("Saved data/materials_cleaned.csv")
