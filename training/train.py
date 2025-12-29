import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

# =========================
# LOAD PREPARED DATA
# =========================

base_path = "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/prepared/"

# ---- COST DATA ----
X_cost_train = pd.read_csv(base_path + "X_cost_train.csv")
X_cost_test  = pd.read_csv(base_path + "X_cost_test.csv")

y_cost_train = pd.read_csv(base_path + "y_cost_train.csv").values.ravel()
y_cost_test  = pd.read_csv(base_path + "y_cost_test.csv").values.ravel()

# ---- CO₂ DATA ----
X_co2_train = pd.read_csv(base_path + "X_co2_train.csv")
X_co2_test  = pd.read_csv(base_path + "X_co2_test.csv")

y_co2_train = pd.read_csv(base_path + "y_co2_train.csv").values.ravel()
y_co2_test  = pd.read_csv(base_path + "y_co2_test.csv").values.ravel()

print("Prepared COST and CO₂ datasets loaded successfully")

# =========================
# COST PREDICTION MODEL
# Random Forest Regressor
# =========================

rf_cost = RandomForestRegressor(
    n_estimators=800,        # higher capacity for ratio learning
    max_depth=None,         # allow full tree growth
    min_samples_split=2,
    min_samples_leaf=1,
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)

rf_cost.fit(X_cost_train, y_cost_train)
y_cost_pred = rf_cost.predict(X_cost_test)

# =========================
# CO₂ IMPACT PREDICTION MODEL
# XGBoost Regressor
# =========================

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

# =========================
# EVALUATION METRICS
# =========================

def evaluate(name, y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae  = mean_absolute_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)

    print(f"\n--- {name} ---")
    print(f"RMSE : {rmse:.4f}")
    print(f"MAE  : {mae:.4f}")
    print(f"R²   : {r2:.4f}")

evaluate("Cost Prediction (Random Forest)", y_cost_test, y_cost_pred)
evaluate("CO₂ Impact Prediction (XGBoost)", y_co2_test, y_co2_pred)

# =========================
# MATERIAL RANKING SYSTEM
# =========================

ranking_df = X_cost_test.copy()

ranking_df["Predicted_Cost_Index"] = y_cost_pred
ranking_df["Predicted_CO2_Index"]  = y_co2_pred

# Lower index = better material
ranking_df["Final_Rank_Score"] = (
    ranking_df["Predicted_Cost_Index"] +
    ranking_df["Predicted_CO2_Index"]
)

ranking_df["Rank"] = ranking_df["Final_Rank_Score"].rank(method="min")
ranking_df = ranking_df.sort_values("Rank")

print("\nTop 5 Recommended Materials:")
print(ranking_df.head(5))

ranking_df.to_csv(
    "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/material_ranking.csv",
    index=False
)

print("\nMODULE 4 COMPLETE: MODEL TRAINING & RANKING DONE")
