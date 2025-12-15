import psycopg2
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
import getpass
import os
import numpy as np
from sqlalchemy import create_engine


db_password = getpass.getpass("Enter PostgreSQL password for 'postgres': ")

engine = create_engine(
    f"postgresql://postgres:{db_password}@localhost/eco_packaging"
)

conn = psycopg2.connect(
    host="localhost",
    database="eco_packaging",
    user="postgres",
    password=db_password
)

print("\nConnected to PostgreSQL!")


mean_imputer = SimpleImputer(strategy="mean")
median_imputer = SimpleImputer(strategy="median")
scaler = StandardScaler()
label_encoders = {}        # store encoders for inference later


def preprocess(df, df_name=""):

    print(f"\n--- PREPROCESSING {df_name} ---")

    # Drop ID columns
    id_cols = [c for c in df.columns if c.lower().endswith("_id")]
    df = df.drop(columns=id_cols, errors="ignore")

    # Detect column types
    categorical = df.select_dtypes(include=['object']).columns.tolist()
    numeric = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    print(f"Categorical columns: {categorical}")
    print(f"Numeric columns: {numeric}")

    # Fill missing categorical values
    df[categorical] = df[categorical].fillna("Unknown")

    # Label Encode ALL categorical columns
    for col in categorical:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Split numeric columns for imputation
    bounded_scores = [c for c in numeric if "score" in c.lower()]
    other_numeric = [c for c in numeric if c not in bounded_scores]

    if bounded_scores:
        df[bounded_scores] = mean_imputer.fit_transform(df[bounded_scores])

    if other_numeric:
        df[other_numeric] = median_imputer.fit_transform(df[other_numeric])

    # Feature engineering for MATERIALS
    if df_name == "MATERIALS":

        if all(col in df.columns for col in 
               ["co2_emission_per_kg", "recyclability_score", "biodegradability_score"]):
            df["CO2_Impact_Index"] = df["co2_emission_per_kg"] / (
                df["recyclability_score"] + df["biodegradability_score"] + 1
            )

        if all(col in df.columns for col in 
               ["durability_score", "cushioning_score", "water_resistance_score",
                "weight_capacity_kg", "cost_per_kg"]):

            df["Performance_Score"] = (
                0.3 * df["durability_score"] +
                0.3 * df["cushioning_score"] +
                0.2 * df["water_resistance_score"] +
                0.2 * df["weight_capacity_kg"]
            )

            df["Cost_Efficiency_Index"] = df["Performance_Score"] / (df["cost_per_kg"] + 1e-6)

        if all(col in df.columns for col in
               ["durability_score", "cushioning_score", "water_resistance_score",
                "recyclability_score", "biodegradability_score"]):

            df["Material_Suitability_Score"] = (
                0.25 * df["durability_score"] +
                0.25 * df["cushioning_score"] +
                0.15 * df["water_resistance_score"] +
                0.20 * df["recyclability_score"] +
                0.15 * df["biodegradability_score"]
            )

        # Add engineered features for scaling
        for col in ["CO2_Impact_Index", "Cost_Efficiency_Index",
                    "Material_Suitability_Score", "Performance_Score"]:
            if col in df.columns:
                numeric.append(col)

    # Log transform skewed columns
    skewed_cols = []
    if "volume_cm3" in df.columns:
        skewed_cols.append("volume_cm3")
    if "price_usd" in df.columns:
        skewed_cols.append("price_usd")

    for col in skewed_cols:
        df[col] = np.log1p(df[col])

    # Standard scale all numeric columns
    df[numeric] = scaler.fit_transform(df[numeric])

    return df



materials = pd.read_sql("SELECT * FROM materials;", engine)
products = pd.read_sql("SELECT * FROM products;", engine)

print("\nDATA LOADED")
print(materials.shape, products.shape)


materials_processed = preprocess(materials, "MATERIALS")
products_processed = preprocess(products, "PRODUCTS")

print("\nPREPROCESSING COMPLETE")


save_path = r"D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/"
os.makedirs(save_path, exist_ok=True)

materials_processed.to_csv(save_path + "processed_materials.csv", index=False)
products_processed.to_csv(save_path + "processed_products.csv", index=False)

print("\nCSVs saved")


print("\n=== FINAL DATA QUALITY VALIDATION ===")
print("\nShapes:")
print(materials_processed.shape, products_processed.shape)

print("\nMissing Values:")
print(materials_processed.isna().sum())
print(products_processed.isna().sum())

print("\nDuplicate Rows:")
print("Materials:", materials_processed.duplicated().sum())
print("Products:", products_processed.duplicated().sum())

print("\nSummary Statistics (Materials):")
print(materials_processed.describe().T)

print("\nSummary Statistics (Products):")
print(products_processed.describe().T)

print("\nSample Rows:")
print(materials_processed.head(3))
print(products_processed.head(3))


conn.close()
print("\nDB Closed")
print("\nDONE")
