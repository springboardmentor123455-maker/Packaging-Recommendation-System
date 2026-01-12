import pandas as pd

def clean_materials():
    # Input & output paths
    input_path = "data/materials.csv"
    output_path = "data/materials_cleaned.csv"

    print("Loading materials data...")
    df = pd.read_csv(input_path)

    print("Columns found:")
    print(df.columns)

    # Keep a copy
    cleaned_df = df.copy()

    # Convert numeric columns safely
    numeric_cols = [
        "strength_kg",
        "weight_g_per_m2",
        "biodegradability_score",
        "co2_emission_kg_per_kg",
        "recyclability_percent",
        "cost_kg",
        "water_resistance_score"
    ]

    for col in numeric_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")

    # Fill missing numeric values with median
    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(
        cleaned_df[numeric_cols].median()
    )

    # Drop rows missing essential text data
    cleaned_df = cleaned_df.dropna(
        subset=["material_name", "material_type"]
    )

    # Reset index
    cleaned_df = cleaned_df.reset_index(drop=True)

    # Save cleaned file
    cleaned_df.to_csv(output_path, index=False)

    print("✅ Cleaned materials data saved to:", output_path)
    print("Final shape:", cleaned_df.shape)


if __name__ == "__main__":
    clean_materials()