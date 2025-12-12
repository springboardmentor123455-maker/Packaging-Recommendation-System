Module 2 — Data Cleaning & Feature Engineering

Milestone: Week 1–2
Project: EcoPackAI – AI-Powered Sustainable Packaging Recommendation System


---

1. Objective

Prepare clean and enriched dataset required for machine learning models by:

Cleaning raw data

Handling missing values

Converting types

Normalizing numeric features

Creating engineered features

Generating a final enriched dataset for model training



---

2. Data Cleaning Steps

2.1 Load the raw dataset

Performed using:

df = pd.read_csv("data/materials.csv")

2.2 Check initial data

df.shape
df.head()
df.isna().sum()
df.dtypes

2.3 Standardize column names

df.columns = [c.strip() for c in df.columns]

2.4 Convert numeric columns

numeric_cols = ["strength_kg","weight_r_per_m2","biodegradability_score",
                "co2_emission_kg_per_kg","recyclability_percent","cost_per_kg","water_resistance_score"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

2.5 Handle missing values

Median is used because it is resistant to outliers.

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

2.6 Save cleaned file

df.to_csv("data/materials_cleaned.csv", index=False)


---

3. Feature Engineering

3.1 CO₂ Impact Index

Lower CO₂ is better.

df["co2_impact_index"] = df["co2_emission_kg_per_kg"]


---

3.2 Cost Efficiency Index

Strength relative to cost.

df["cost_efficiency_index"] = df["strength_kg"] / (df["cost_per_kg"] + 1e-6)


---

3.3 Recyclability Normalization

df["recyclability_norm"] = df["recyclability_percent"] / 100


---

3.4 Normalize values (0–1 scale)

scaler = MinMaxScaler()
df[["co2_impact_index","cost_efficiency_index","biodegradability_score","recyclability_norm","water_resistance_score"]] = \
    scaler.fit_transform(df[["co2_impact_index","cost_efficiency_index","biodegradability_score","recyclability_norm","water_resistance_score"]])


---

3.5 Material Suitability Score (Weighted Formula)

Formula used:

0.30 * biodegradability
0.20 * recyclability
0.25 * cost efficiency
0.15 * water resistance
-0.10 * CO₂ impact

Code:

df["material_suitability_score"] = (
    0.30 * df["biodegradability_score"] +
    0.20 * df["recyclability_norm"] +
    0.25 * df["cost_efficiency_index"] +
    0.15 * df["water_resistance_score"] -
    0.10 * df["co2_impact_index"]
)

Normalize suitability:

df["material_suitability_score"] = MinMaxScaler().fit_transform(df[["material_suitability_score"]])


---

3.6 Save engineered dataset

df.to_csv("data/materials_engineered.csv", index=False)


---

4. Validation Checks

Check	Description

Missing values	All must be filled
material_suitability_score	Should be within 0–1
Column types	Numeric columns must be float
Outliers	Verified using .describe()
Sorting	Top materials visible



---

5. Outputs for Module 2

✔ materials_cleaned.csv
✔ materials_engineered.csv
✔ Added new features:

co2_impact_index

cost_efficiency_index

material_suitability_score