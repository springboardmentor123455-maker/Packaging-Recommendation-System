import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# STEP 1: Load prepared data
X_train = pd.read_csv("data/X_train.csv")
X_test = pd.read_csv("data/X_test.csv")

y_cost_train = pd.read_csv("data/y_cost_train.csv").values.ravel()
y_cost_test = pd.read_csv("data/y_cost_test.csv").values.ravel()

y_co2_train = pd.read_csv("data/y_co2_train.csv").values.ravel()
y_co2_test = pd.read_csv("data/y_co2_test.csv").values.ravel()

df_original = pd.read_csv("data/materials_cleaned.csv")

print("\n Prepared data loaded")

# STEP 2: Cost Prediction – Random Forest
cost_model = RandomForestRegressor(random_state=42)
cost_model.fit(X_train, y_cost_train)
cost_pred = cost_model.predict(X_test)

# STEP 3: CO₂ Prediction – Gradient Boosting (XGBoost alternative)
co2_model = GradientBoostingRegressor(random_state=42)
co2_model.fit(X_train, y_co2_train)
co2_pred = co2_model.predict(X_test)

# STEP 4: Evaluation Function
def evaluate(y_true, y_pred, name):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print(f"\n {name} Model Evaluation")
    print("RMSE:", rmse)
    print("MAE :", mae)
    print("R2  :", r2)

evaluate(y_cost_test, cost_pred, "Cost Prediction (Random Forest)")
evaluate(y_co2_test, co2_pred, "CO₂ Prediction (Gradient Boosting)")

# STEP 5: Predict for all materials
df_original["predicted_cost"] = cost_model.predict(pd.concat([X_train, X_test]))
df_original["predicted_co2"] = co2_model.predict(pd.concat([X_train, X_test]))

# STEP 6: Ranking system
df_original["final_score"] = (
    df_original["predicted_cost"].rank(ascending=True) +
    df_original["predicted_co2"].rank(ascending=True)
)

df_original["Rank"] = df_original["final_score"].rank(method="dense")

# STEP 7: Show Top 10
print("\n Top 10 Ranked Eco-Friendly Materials:\n")
print(
    df_original.sort_values("Rank")[
        ["Rank", "material_name", "predicted_cost", "predicted_co2"]
    ].head(10)
)

# STEP 8: Save output
df_original.to_csv("data/final_recommendations.csv", index=False)

print("\n Module 4 AI Recommendation Completed")