import pandas as pd

df = pd.read_csv("data/materials_cleaned.csv")

df["co2_impact_index"] = df["co2_emission_kg_per_kg"] * (1 - df["recyclability_percent"]/100)
df["cost_efficiency_index"] = df["strength_kg"] / df["cost_per_kg"]
df["material_suitability_score"] = (
    0.4 * df["biodegradability_score"] +
    0.3 * df["recyclability_percent"]/100 +
    0.3 * (1 / (1 + df["co2_emission_kg_per_kg"]))
)

df.to_csv("data/materials_engineered.csv", index=False)

print("Feature engineering complete!")
print(df.head())