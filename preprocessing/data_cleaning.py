import psycopg2
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
import getpass
import os
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt



# DATABASE CONNECTION

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



# PREPROCESSING TOOLS

mean_imputer = SimpleImputer(strategy="mean")
median_imputer = SimpleImputer(strategy="median")
scaler = StandardScaler()
label_encoders = {}



# PREPROCESS FUNCTION

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

    # Handle missing categorical values
    df[categorical] = df[categorical].fillna("Unknown")

    # Label encoding
    for col in categorical:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Numeric imputation
    bounded_scores = [c for c in numeric if "score" in c.lower()]
    other_numeric = [c for c in numeric if c not in bounded_scores]

    if bounded_scores:
        df[bounded_scores] = mean_imputer.fit_transform(df[bounded_scores])

    if other_numeric:
        df[other_numeric] = median_imputer.fit_transform(df[other_numeric])

    
    # FEATURE ENGINEERING (MATERIALS)
    
    if df_name == "MATERIALS":

        if all(col in df.columns for col in
               ["co2_emission_per_kg", "recyclability_score", "biodegradability_score"]):
            df["CO2_Impact_Index"] = df["co2_emission_per_kg"] / (
                df["recyclability_score"] + df["biodegradability_score"] + 1
            )

        if all(col in df.columns for col in
               ["durability_score", "cushioning_score",
                "water_resistance_score", "weight_capacity_kg"]):
            df["Performance_Score"] = (
                0.3 * df["durability_score"] +
                0.3 * df["cushioning_score"] +
                0.2 * df["water_resistance_score"] +
                0.2 * df["weight_capacity_kg"]
            )

        if "cost_per_kg" in df.columns:
            df["Cost_Efficiency_Index"] = df["Performance_Score"] / (df["cost_per_kg"] + 1e-6)

        if all(col in df.columns for col in
               ["durability_score", "cushioning_score",
                "water_resistance_score",
                "recyclability_score", "biodegradability_score"]):
            df["Material_Suitability_Score"] = (
                0.25 * df["durability_score"] +
                0.25 * df["cushioning_score"] +
                0.15 * df["water_resistance_score"] +
                0.20 * df["recyclability_score"] +
                0.15 * df["biodegradability_score"]
            )

        for col in [
            "CO2_Impact_Index",
            "Performance_Score",
            "Cost_Efficiency_Index",
            "Material_Suitability_Score"
        ]:
            if col in df.columns:
                numeric.append(col)

    # Log transform skewed columns
    for col in ["volume_cm3", "price_usd"]:
        if col in df.columns:
            df[col] = np.log1p(df[col])

    # Standard scaling
    df[numeric] = scaler.fit_transform(df[numeric])

    return df


# LOAD DATA

materials = pd.read_sql("SELECT * FROM materials;", engine)
products = pd.read_sql("SELECT * FROM products;", engine)

print("\nDATA LOADED")
print(materials.shape, products.shape)


materials_processed = preprocess(materials, "MATERIALS")
products_processed = preprocess(products, "PRODUCTS")

print("\nPREPROCESSING COMPLETE")



# SAVE CSVs

save_path = r"D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/"
os.makedirs(save_path, exist_ok=True)

materials_processed.to_csv(save_path + "processed_materials.csv", index=False)
products_processed.to_csv(save_path + "processed_products.csv", index=False)

print("\nCSVs saved")



# DATA QUALITY VALIDATION

print("\n=== DATA QUALITY VALIDATION ===")

print("\nShapes:")
print(materials_processed.shape, products_processed.shape)

print("\nMissing Values:")
print(materials_processed.isna().sum())
print(products_processed.isna().sum())

print("\nDuplicate Rows:")
print("Materials:", materials_processed.duplicated().sum())
print("Products:", products_processed.duplicated().sum())

print("\nSummary Statistics (Materials):")
materials_stats = materials_processed.describe().T
print(materials_stats)

print("\nSummary Statistics (Products):")
products_stats = products_processed.describe().T
print(products_stats)

# Zero-variance feature check
print("\nZero-Variance Features (Materials):")
print(materials_stats[materials_stats["std"] == 0].index.tolist())



# CORRELATION ANALYSIS & CHARTS

def plot_correlation(df, title, filename):

    corr = df.corr()

    plt.figure(figsize=(12, 10))
    plt.imshow(corr, interpolation='nearest')
    plt.title(title)
    plt.colorbar()

    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)

    plt.tight_layout()
    plt.savefig(save_path + filename)
    plt.close()

    print(f"Correlation heatmap saved: {filename}")


plot_correlation(
    materials_processed,
    "Feature Correlation Matrix – Materials",
    "materials_correlation.png"
)

plot_correlation(
    products_processed,
    "Feature Correlation Matrix – Products",
    "products_correlation.png"
)



# SAMPLE ROWS

print("\nSample Rows (Materials):")
print(materials_processed.head(3))

print("\nSample Rows (Products):")
print(products_processed.head(3))



# CLEANUP

conn.close()
print("\nDB Closed")
print("\nDONE")
