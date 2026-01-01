import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

# =========================================================
# LOAD DATASET
# =========================================================
df = pd.read_csv("processed_materials.csv")

# =========================================================
# MODULE 3: ML DATASET PREPARATION
# =========================================================

# Feature selection (material safety, strength, category)
feature_cols = [
    'Material_Suitability_Score',
    'Strength',
    'Material_Type_Aluminum',
    'Material_Type_Bamboo',
    'Material_Type_Cotton',
    'Material_Type_Glass',
    'Material_Type_Paper',
    'Material_Type_Plastic',
    'Material_Type_Steel',
    'Material_Type_Wood'
]

X = df[feature_cols]
# Clip extreme cost values (outlier control)
upper_limit = y_cost.quantile(0.95)
y_cost_clipped = y_cost.clip(upper=upper_limit)
# Targets
y_cost = y_cost_clipped

y_co2 = df['CO2_Impact_Index']



# Train-test split
X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

_, _, y_co2_train, y_co2_test = train_test_split(
    X, y_co2, test_size=0.2, random_state=42
)

# =========================================================
# MODULE 4: AI RECOMMENDATION MODELS
# =========================================================

# ---- COST PREDICTION: RANDOM FOREST REGRESSOR ----
cost_model = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ))
])

cost_model.fit(X_train, y_cost_train)
cost_preds = cost_model.predict(X_test)

# Cost evaluation
cost_rmse = np.sqrt(mean_squared_error(y_cost_test, cost_preds))
cost_mae = mean_absolute_error(y_cost_test, cost_preds)
cost_r2 = r2_score(y_cost_test, cost_preds)

# ---- CO2 IMPACT PREDICTION: XGBOOST REGRESSOR ----
co2_model = Pipeline([
    ('scaler', StandardScaler()),
    ('model', XGBRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    ))
])

co2_model.fit(X_train, y_co2_train)
co2_preds = co2_model.predict(X_test)

# CO2 evaluation
co2_rmse = np.sqrt(mean_squared_error(y_co2_test, co2_preds))
co2_mae = mean_absolute_error(y_co2_test, co2_preds)
co2_r2 = r2_score(y_co2_test, co2_preds)

# =========================================================
# EVALUATION OUTPUT
# =========================================================
print("\n========= MODEL EVALUATION RESULTS =========\n")

print("COST PREDICTION (Random Forest)")
print("RMSE:", round(cost_rmse, 4))
print("MAE :", round(cost_mae, 4))
print("R2  :", round(cost_r2, 4))

print("\nCO2 IMPACT PREDICTION (XGBoost)")
print("RMSE:", round(co2_rmse, 4))
print("MAE :", round(co2_mae, 4))
print("R2  :", round(co2_r2, 4))

# =========================================================
# AI MATERIAL RANKING SYSTEM
# =========================================================

df['Predicted_Cost'] = cost_model.predict(X)
df['Predicted_CO2'] = co2_model.predict(X)

# Normalize predictions
df['Cost_Score'] = (df['Predicted_Cost'] - df['Predicted_Cost'].min()) / (
    df['Predicted_Cost'].max() - df['Predicted_Cost'].min()
)

df['CO2_Score'] = (df['Predicted_CO2'] - df['Predicted_CO2'].min()) / (
    df['Predicted_CO2'].max() - df['Predicted_CO2'].min()
)

# Final ranking score
df['Material_Rank'] = 1 - (0.5 * df['Cost_Score'] + 0.5 * df['CO2_Score'])

df = df.sort_values(by='Material_Rank', ascending=False)
df['Material_Rank_Position'] = range(1, len(df) + 1)

# Save results
df.to_csv("ai_material_recommendations.csv", index=False)

print("\n AI Material Recommendation System_new2 Completed")
