import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def clean_and_engineer_materials(
    input_path: str = "data/materials.csv",
    output_path: str = "data/materials_cleaned.csv",
):
    # 1. Load Raw Data -------------------------------------------------
    print(f"\nLoading raw materials data from: {input_path}")
    df = pd.read_csv(input_path)

    print("\n--- RAW DATA PREVIEW ---")
    print(df.head())
    print("\nShape:", df.shape)
    print("\nMissing values BEFORE conversion:")
    print(df.isna().sum())

    # 2. Convert numeric columns safely --------------------------------
    numeric_cols = [
        "strength_kg",
        "weight_g_per_m2",
        "biodegradability_score",
        "co2_emission_kg_per_kg",
        "recyclability_percent",
        "cost_kg",          # ✅ correct column name
    ]

    # Convert to numeric (anything invalid -> NaN)
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print("\nMissing values AFTER numeric conversion:")
    print(df[numeric_cols].isna().sum())

    # 3. Handle Missing Values (median) --------------------------------
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    print("\nMissing values AFTER filling (median):")
    print(df[numeric_cols].isna().sum())

    # 4. Normalization with MinMaxScaler -------------------------------
    scaler = MinMaxScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    print("\n--- Normalized data preview ---")
    print(df.head())

    # 5. Feature Engineering -------------------------------------------
    # Cost efficiency: high strength, low cost_kg
    df["cost_efficiency_index"] = df["strength_kg"] / (df["cost_kg"] + 0.0001)

    # Sustainability score: biodegradability + recyclability
    df["sustainability_score"] = (
        df["biodegradability_score"] * 0.6
        + df["recyclability_percent"] * 0.4
    )

    # Overall material suitability for eco-packaging
    df["material_suitability"] = (
        df["sustainability_score"] * 0.6
        + df["cost_efficiency_index"] * 0.4
    )

    print("\n--- Feature engineered columns (preview) ---")
    print(df[["cost_efficiency_index",
              "sustainability_score",
              "material_suitability"]].head())

    # 6. Outlier / Stats Check -----------------------------------------
    print("\n--- Describe stats (for outlier check) ---")
    print(df[numeric_cols + [
        "cost_efficiency_index",
        "sustainability_score",
        "material_suitability",
    ]].describe())

    # 7. Save Cleaned & Engineered Data --------------------------------
    df.to_csv(output_path, index=False)
    print(f"\nCLEANED & ENGINEERED DATA saved to: {output_path}")


if __name__ == "__main__":
    clean_and_engineer_materials()
