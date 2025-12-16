import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib
import os

# ==============================
# STEP 1: LOAD DATA
# ==============================
DATA_FOLDER = "data"

X_train = pd.read_csv(os.path.join(DATA_FOLDER, "X_train.csv"))
X_test = pd.read_csv(os.path.join(DATA_FOLDER, "X_test.csv"))

y_train = pd.read_csv(os.path.join(DATA_FOLDER, "y_suitability_train.csv"))
y_test = pd.read_csv(os.path.join(DATA_FOLDER, "y_suitability_test.csv"))

print("✔ Training data loaded")
print("X_train shape:", X_train.shape)

# Convert y to 1D array
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()

# ==============================
# STEP 2: TRAIN MODEL
# ==============================
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

print("\n🔹 Training Random Forest model...")
model.fit(X_train, y_train)

# ==============================
# STEP 3: PREDICTIONS
# ==============================
y_pred = model.predict(X_test)

# ==============================
# STEP 4: EVALUATION METRICS
# ==============================
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📊 MODEL EVALUATION RESULTS")
print("MAE :", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R²  :", round(r2, 4))

# ==============================
# STEP 5: SAVE MODEL
# ==============================
joblib.dump(model, os.path.join(DATA_FOLDER, "material_suitability_model.pkl"))
print("\n💾 Model saved as material_suitability_model.pkl")
