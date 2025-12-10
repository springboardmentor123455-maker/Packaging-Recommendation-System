import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ------------------------------
# 1. Load Raw Data
# ------------------------------
df = pd.read_csv("data/materials.csv")

print("\n--- RAW DATA PREVIEW ---")
print(df.head())
print("\nShape:", df.shape)
print("\nMissing values BEFORE:", df.isna().sum())


# ------------------------------
# 2. Convert numeric columns
# ------------------------------
num_cols = [
    "strength_kg",
    "weight_g_per_m2",
    "biodegradability_score",
    "co2_emission_kg_per_kg",
    "recyclability_percent",
    "unit_cost"
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nMissing values AFTER conversion:", df.isna().sum())


# ------------------------------
# 3. Handle Missing Values
# ------------------------------
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

print("\nMissing values AFTER filling:", df.isna().sum())


# ------------------------------
# 4. Normalization using MinMax
# ------------------------------
scaler = MinMaxScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

print("\n--- Normalized Data Preview ---")
print(df.head())


# ------------------------------
# 5. Feature Engineering
# ------------------------------
# Cost efficiency
df['cost_efficiency_index'] = df['strength_kg'] / (df['unit_cost'] + 0.0001)

# Sustainability score
df['sustainability_score'] = (
    df['biodegradability_score'] * 0.6 +
    df['recyclability_percent'] * 0.4
)

# Material suitability
df['material_suitability'] = (
    df['sustainability_score'] * 0.6 +
    df['cost_efficiency_index'] * 0.4
)

print("\n--- Feature Engineered Columns ---")
print(df[['cost_efficiency_index', 'sustainability_score', 'material_suitability']].head())


# ------------------------------
# 6. Outlier / Stats Validation
# ------------------------------
print("\n--- Describe (outlier check) ---")
print(df.describe())


# ------------------------------
# 7. Save Cleaned Data
# ------------------------------
df.to_csv("data/materials_cleaned.csv", index=False)
print("\nCLEANED DATA saved to data/materials_cleaned.csv")