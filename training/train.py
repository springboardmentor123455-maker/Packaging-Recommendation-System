import pandas as pd
import numpy as np
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

# PATHS

BASE_PREP = "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/prepared/"
OUTPUT_DIR  = "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/"


#  EXPLICIT RAW CSV PATHS 


RAW_PRODUCTS_CSV  = r"D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/products_.csv"
RAW_MATERIALS_CSV = r"D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/materials_.csv"

# ---- SAFETY CHECK ----
if not os.path.exists(RAW_PRODUCTS_CSV):
    raise FileNotFoundError(f"Product CSV not found at: {RAW_PRODUCTS_CSV}")

if not os.path.exists(RAW_MATERIALS_CSV):
    raise FileNotFoundError(f"Materials CSV not found at: {RAW_MATERIALS_CSV}")


# PART 1: MATERIAL-ONLY MODELS 


# ---- COST DATA ----
X_cost_train = pd.read_csv(BASE_PREP + "X_cost_train.csv")
X_cost_test  = pd.read_csv(BASE_PREP + "X_cost_test.csv")
y_cost_train = pd.read_csv(BASE_PREP + "y_cost_train.csv").values.ravel()
y_cost_test  = pd.read_csv(BASE_PREP + "y_cost_test.csv").values.ravel()

# ---- CO₂ DATA ----
X_co2_train = pd.read_csv(BASE_PREP + "X_co2_train.csv")
X_co2_test  = pd.read_csv(BASE_PREP + "X_co2_test.csv")
y_co2_train = pd.read_csv(BASE_PREP + "y_co2_train.csv").values.ravel()
y_co2_test  = pd.read_csv(BASE_PREP + "y_co2_test.csv").values.ravel()

print("Prepared COST and CO₂ datasets loaded successfully")

# ---- COST MODEL ----
rf_cost = RandomForestRegressor(
    n_estimators=800,
    random_state=42,
    n_jobs=-1
)
rf_cost.fit(X_cost_train, y_cost_train)
y_cost_pred = rf_cost.predict(X_cost_test)

# ---- CO₂ MODEL ----
xgb_co2 = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.07,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="reg:squarederror",
    random_state=42
)
xgb_co2.fit(X_co2_train, y_co2_train)
y_co2_pred = xgb_co2.predict(X_co2_test)

# ---- EVALUATION ----
def evaluate(name, y_true, y_pred):
    print(f"\n--- {name} ---")
    print(f"RMSE : {np.sqrt(mean_squared_error(y_true, y_pred)):.4f}")
    print(f"MAE  : {mean_absolute_error(y_true, y_pred):.4f}")
    print(f"R²   : {r2_score(y_true, y_pred):.4f}")

evaluate("Cost Prediction (Random Forest)", y_cost_test, y_cost_pred)
evaluate("CO₂ Impact Prediction (XGBoost)", y_co2_test, y_co2_pred)

# ---- GLOBAL MATERIAL RANKING ----
ranking_global = X_cost_test.copy()
ranking_global["Predicted_Cost_Index"] = y_cost_pred
ranking_global["Predicted_CO2_Index"]  = y_co2_pred
ranking_global["Final_Rank_Score"] = (
    ranking_global["Predicted_Cost_Index"] +
    ranking_global["Predicted_CO2_Index"]
)
ranking_global["Rank"] = ranking_global["Final_Rank_Score"].rank(method="min")
ranking_global = ranking_global.sort_values("Rank")

# ---- ATTACH MATERIAL NAMES ----
raw_materials = pd.read_csv(RAW_MATERIALS_CSV)

ranking_global["material_name"] = raw_materials.loc[
    ranking_global.index % len(raw_materials),
    "material_name"
].values

print("\nTop 5 Recommended Materials (GLOBAL):")
print(ranking_global[["material_name", "Final_Rank_Score", "Rank"]].head(5))

ranking_global.to_csv(
    OUTPUT_DIR + "material_ranking_named.csv",
    index=False
)


# PART 2: PRODUCT–MATERIAL MODEL 


X_pm_train = pd.read_csv(BASE_PREP + "X_pm_train.csv")
X_pm_test  = pd.read_csv(BASE_PREP + "X_pm_test.csv")
y_pm_train = pd.read_csv(BASE_PREP + "y_pm_train.csv").values.ravel()
y_pm_test  = pd.read_csv(BASE_PREP + "y_pm_test.csv").values.ravel()

print("\nProduct–Material training data loaded")
print("Train:", X_pm_train.shape, "Test:", X_pm_test.shape)

xgb_pm = XGBRegressor(
    n_estimators=350,
    max_depth=5,
    learning_rate=0.06,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="reg:squarederror",
    random_state=42
)

xgb_pm.fit(X_pm_train, y_pm_train)
y_pm_pred = xgb_pm.predict(X_pm_test)

evaluate("Product–Material Suitability (XGBoost)", y_pm_test, y_pm_pred)


# PART 3: USER-SELECTABLE PRODUCT-SPECIFIC RANKING


raw_products = pd.read_csv(RAW_PRODUCTS_CSV)

print("\nAvailable Products:")
for i, name in enumerate(raw_products["product_name"].head(10)):
    print(f"{i}: {name}")

product_index = int(input("\nEnter product index to recommend materials for: "))
selected_product_name = raw_products.iloc[product_index]["product_name"]

print(f"\nSelected Product: {selected_product_name}")

# Predict suitability for all PM test rows
pm_rank = X_pm_test.copy()
pm_rank["Predicted_Suitability"] = y_pm_pred

# Attach material names
material_count = len(raw_materials)
pm_rank["material_name"] = [
    raw_materials.iloc[i % material_count]["material_name"]
    for i in range(len(pm_rank))
]

# Aggregate per material
product_ranking = (
    pm_rank
    .groupby("material_name")["Predicted_Suitability"]
    .mean()
    .reset_index()
    .sort_values("Predicted_Suitability", ascending=False)
)

print(f"\nTop 5 Materials for Product: {selected_product_name}")
print(product_ranking.head(5))

product_ranking.to_csv(
    OUTPUT_DIR + "product_material_ranking_named.csv",
    index=False
)

print("\nMODULE 4 COMPLETE: GLOBAL + PRODUCT-SPECIFIC ML RECOMMENDATIONS READY")
