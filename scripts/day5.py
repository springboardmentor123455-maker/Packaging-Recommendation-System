import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

# -----------------------------
# STEP 1: Resolve project paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RAW_FILE = DATA_DIR / "materials_raw.csv"
CLEAN_FILE = DATA_DIR / "clean_materials.csv"
OUTPUT_FILE = DATA_DIR / "feature_engineered_materials.csv"

# -----------------------------
# STEP 2: Ensure clean_materials.csv exists
# -----------------------------
if CLEAN_FILE.exists():
    print("✔ Found clean_materials.csv")
    df = pd.read_csv(CLEAN_FILE)
else:
    print("⚠ clean_materials.csv not found. Creating it from raw data...")

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            "materials_raw.csv not found inside data folder"
        )

    df = pd.read_csv(RAW_FILE)

    # Basic cleaning (Day 4 logic)
    df.drop_duplicates(inplace=True)
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Rename columns (important)
    df.rename(columns={
        'Material_Type': 'material_type',
        'Strength_MPa': 'strength',
        'Weight_Capacity_kg': 'weight_capacity',
        'Biodegradability_Score': 'biodegradability',
        'CO2_Emission_Score': 'co2_emission',
        'Recyclability_Percent': 'recyclability'
    }, inplace=True)

    # Encode categorical column
    df = pd.get_dummies(df, columns=['material_type'], drop_first=True)

    # Save clean file
    df.to_csv(CLEAN_FILE, index=False)
    print("✔ clean_materials.csv created successfully")

# -----------------------------
# STEP 3: Feature Engineering (Day 5)
# -----------------------------

# CO2 Impact Index (lower CO2 = higher score)
df['co2_impact_index'] = 100 - (df['co2_emission'] * 10)

# Cost Efficiency Index (proxy)
df['cost_efficiency_index'] = df['strength'] / df['weight_capacity']

# Normalize numerical features
scaler = MinMaxScaler()

scale_columns = [
    'strength',
    'weight_capacity',
    'biodegradability',
    'recyclability',
    'co2_impact_index',
    'cost_efficiency_index'
]

df[scale_columns] = scaler.fit_transform(df[scale_columns])

# Material Suitability Score
df['material_suitability_score'] = (
    df['strength'] * 0.25 +
    df['biodegradability'] * 0.30 +
    df['recyclability'] * 0.20 +
    df['co2_impact_index'] * 0.25
)

# Rank materials
df['rank'] = df['material_suitability_score'].rank(
    ascending=False, method='dense'
)

# -----------------------------
# STEP 4: Save output
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print("🎉 Day 5 completed successfully")
print(f"📁 Output saved at: {OUTPUT_FILE}")
