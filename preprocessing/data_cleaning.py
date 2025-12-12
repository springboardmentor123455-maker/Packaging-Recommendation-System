import psycopg2
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import getpass
import os
import numpy as np
from sqlalchemy import create_engine


# Connect to PostgreSQL

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



# Initialize imputers and scaler

mean_imputer = SimpleImputer(strategy="mean")       
median_imputer = SimpleImputer(strategy="median")   
scaler = StandardScaler()                          


# Main preprocessing function

def preprocess(df, df_name=""):
    """
    Cleans and enriches material/product data.
    Handles missing values, feature engineering,
    normalization, and prepares dataset for ML models.
    """

    print(f"\n--- PREPROCESSING {df_name} ---")

    
    # 1) Drop ID columns
    
    id_cols = [c for c in df.columns if c.lower().endswith("_id")]
    df = df.drop(columns=id_cols, errors="ignore")

    
    # 2) Identify column types
   
    categorical = df.select_dtypes(include=['object']).columns.tolist()
    numeric = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    print(f"Categorical columns: {categorical}")
    print(f"Numeric columns: {numeric}")

    
    # 3) Handle missing categorical values
    # Fill with "Unknown" because categories are mostly unique
    #
    df[categorical] = df[categorical].fillna("Unknown")

    
    # 4) Split numeric columns into score-based & others
    # Score columns (0–10) get mean imputation
    # Other numeric features get median imputation
    
    bounded_scores = [c for c in numeric if "score" in c.lower()]
    other_numeric = [c for c in numeric if c not in bounded_scores]

    # Impute each group appropriately
    if bounded_scores:
        df[bounded_scores] = mean_imputer.fit_transform(df[bounded_scores])

    if other_numeric:
        df[other_numeric] = median_imputer.fit_transform(df[other_numeric])

    
    # 5) Feature Engineering 
    
    if df_name == "MATERIALS":

        
        # CO₂ Impact Index
        # Measures how harmful a material is environmentally
        
        if all(col in df.columns for col in 
               ["co2_emission_per_kg", "recyclability_score", "biodegradability_score"]):
            df["CO2_Impact_Index"] = df["co2_emission_per_kg"] / (
                df["recyclability_score"] + df["biodegradability_score"] + 1
            )

     
        # Cost Efficiency Index
        # Combines performance characteristics relative to cost
        
        if all(col in df.columns for col in 
               ["durability_score", "cushioning_score", "water_resistance_score", 
                "weight_capacity_kg", "cost_per_kg"]):

            # Weighted performance score
            df["Performance_Score"] = (
                0.3 * df["durability_score"] +
                0.3 * df["cushioning_score"] +
                0.2 * df["water_resistance_score"] +
                0.2 * df["weight_capacity_kg"]
            )

            df["Cost_Efficiency_Index"] = df["Performance_Score"] / (df["cost_per_kg"] + 1e-6)

       
        # Material Suitability Score
        # Represents how good a material is overall for packaging
        
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

        # Add new engineered features into numeric list for scaling
        for col in ["CO2_Impact_Index", "Cost_Efficiency_Index", 
                    "Material_Suitability_Score", "Performance_Score"]:
            if col in df.columns:
                numeric.append(col)

    
    # 6) Log-transform skewed columns
    # Reduces extreme range differences (esp. volume & price)
    
    skewed_cols = []
    if "volume_cm3" in df.columns: 
        skewed_cols.append("volume_cm3")
    if "price_usd" in df.columns: 
        skewed_cols.append("price_usd")

    for col in skewed_cols:
        df[col] = np.log1p(df[col])  

    
    # 7) Standardize all numeric features
    # Makes features comparable for ML algorithms
    
    df[numeric] = scaler.fit_transform(df[numeric])

    return df


# Load data from database

materials = pd.read_sql("SELECT * FROM materials;", engine)
products = pd.read_sql("SELECT * FROM products;", engine)

print("\nDATA LOADED")
print(materials.shape, products.shape)



# Run preprocessing

materials_processed = preprocess(materials, "MATERIALS")
products_processed = preprocess(products, "PRODUCTS")

print("\nPREPROCESSING COMPLETE")



# Save processed data to CSV

save_path = r"D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/"
os.makedirs(save_path, exist_ok=True)

materials_processed.to_csv(save_path + "processed_materials.csv", index=False)
products_processed.to_csv(save_path + "processed_products.csv", index=False)

print("\n CSVs saved")



# Final Data Validation Summary

print("\n=== FINAL DATA QUALITY VALIDATION ===")

print("\n1️ Shapes:")
print(materials_processed.shape, products_processed.shape)

print("\n2️ Missing Values:")
print(materials_processed.isna().sum())
print(products_processed.isna().sum())

print("\n3️ Duplicate Rows:")
print("Materials:", materials_processed.duplicated().sum())
print("Products:", products_processed.duplicated().sum())

print("\n4️ Summary Statistics (Materials):")
print(materials_processed.describe().T)

print("\n5️ Summary Statistics (Products):")
print(products_processed.describe().T)

print("\n6️ Sample Rows:")
print(materials_processed.head(3))
print(products_processed.head(3))


# Close DB connection

conn.close()
print("\n DB Closed")
print("\n DONE")
