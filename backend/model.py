import joblib
import os
import pandas as pd

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
PREP_DIR = os.path.join(DATA_DIR, "prepared")
MODEL_DIR = os.path.join(BASE_DIR, "trained_models")

print("Looking for models in:", MODEL_DIR)

# Load models
cost_model = joblib.load(os.path.join(MODEL_DIR, "cost_model.pkl"))
co2_model  = joblib.load(os.path.join(MODEL_DIR, "co2_model.pkl"))
pm_model   = joblib.load(os.path.join(MODEL_DIR, "pm_model.pkl"))

print("All models loaded")

# Load prepared PM data + lookup tables
X_pm = pd.read_csv(os.path.join(PREP_DIR, "X_pm_test.csv"))
products  = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
materials = pd.read_csv(os.path.join(DATA_DIR, "materials.csv"))

material_count = len(materials)
rows_per_product = len(X_pm) // len(products)

# ---------------------------
# BASIC PREDICTION FUNCTIONS
# ---------------------------

def predict_cost(X):
    return cost_model.predict(X)

def predict_co2(X):
    return co2_model.predict(X)

def predict_pm(X):
    return pm_model.predict(X)

# ---------------------------
#PRODUCT-AWARE RANKING
# ---------------------------

def rank_materials_for_product(product_name):

    matches = products[products["product_name"] == product_name]
    if matches.empty:
        return None

    p_idx = matches.index[0]

    start = p_idx * rows_per_product
    end   = start + rows_per_product

    subset = X_pm.iloc[start:end].copy()

    preds = pm_model.predict(subset)
    subset["Predicted_Suitability"] = preds

    subset["material_name"] = [
        materials.iloc[i % material_count]["material_name"]
        for i in range(len(subset))
    ]

    ranking = (
        subset
        .groupby("material_name")["Predicted_Suitability"]
        .mean()
        .reset_index()
        .sort_values("Predicted_Suitability", ascending=False)
        .head(5)
    )

    return ranking.to_dict(orient="records")
