📦 EcoPackAI
Module 4: AI Recommendation Model (ML-Based)

(Cost Prediction, CO₂ Footprint Prediction & Material Ranking)

📌 Module Overview

Module 4 is the core intelligence layer of EcoPackAI.
It trains machine learning models to:

Predict packaging material cost

Predict CO₂ footprint

Rank packaging materials based on sustainability and efficiency

This module converts ML predictions into actionable material recommendations.

🎯 Objectives

Train ML models for:

Cost prediction

CO₂ emission prediction

Evaluate models using standard regression metrics

Generate a material ranking system

Save trained models for backend/API integration

🔄 Input & Output
🔹 Input

ML-ready datasets from Module 3:

X_train.csv, X_test.csv

y_cost_train.csv, y_cost_test.csv

y_co2_train.csv, y_co2_test.csv

🔹 Output

Trained ML models (.pkl)

Evaluation metrics (RMSE, MAE, R²)

Ranked materials dataset

🗂 Folder Structure
EcoPackAI/
└── module4_ai_model/
    ├── data/
    │   ├── X_train.csv
    │   ├── X_test.csv
    │   ├── y_cost_train.csv
    │   ├── y_cost_test.csv
    │   ├── y_co2_train.csv
    │   └── y_co2_test.csv
    ├── models/
    │   ├── cost_model.pkl
    │   └── co2_model.pkl
    ├── training/
    │   ├── train_cost_model.py
    │   ├── train_co2_model.py
    │   └── evaluate_models.py
    ├── ranking/
    │   └── material_ranking.py
    └── README.md

🛠 Packages Used
Package	Version
python	3.10
pandas	2.1.1
numpy	1.26.2
scikit-learn	1.3.2
xgboost	2.0.2
joblib	1.3.2
⚙️ Installation
pip install pandas==2.1.1 numpy==1.26.2 scikit-learn==1.3.2 xgboost==2.0.2 joblib==1.3.2

🤖 Model Selection Rationale
Task	Model Used	Reason
Cost Prediction	Random Forest Regressor	Handles non-linearity, robust to outliers
CO₂ Prediction	XGBoost Regressor	High accuracy, strong generalization
🧠 Step 1: Cost Prediction Model

File: train_cost_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_cost_model():
    X_train = pd.read_csv("data/X_train.csv")
    y_train = pd.read_csv("data/y_cost_train.csv")

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    model.fit(X_train, y_train.values.ravel())

    joblib.dump(model, "models/cost_model.pkl")
    return model

🔧 Functions Used
Function	Usage
RandomForestRegressor()	Train cost prediction model
fit()	Model training
joblib.dump()	Save trained model
🌱 Step 2: CO₂ Footprint Prediction Model

File: train_co2_model.py

import pandas as pd
from xgboost import XGBRegressor
import joblib

def train_co2_model():
    X_train = pd.read_csv("data/X_train.csv")
    y_train = pd.read_csv("data/y_co2_train.csv")

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train.values.ravel())

    joblib.dump(model, "models/co2_model.pkl")
    return model

📊 Step 3: Model Evaluation

File: evaluate_models.py

Metrics Used

RMSE – Prediction error magnitude

MAE – Average absolute error

R² Score – Model explanatory power

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return rmse, mae, r2

🏆 Step 4: Material Recommendation Ranking

File: material_ranking.py

Ranking Logic
Final Score =
(1 / Predicted Cost) +
(1 / Predicted CO₂) +
Material Suitability Score

def rank_materials(df):
    df["final_score"] = (
        (1 / df["predicted_cost"]) +
        (1 / df["predicted_co2"]) +
        df["material_suitability_score"]
    )

    return df.sort_values("final_score", ascending=False)

▶️ How to Run Module 4
python training/train_cost_model.py
python training/train_co2_model.py
python training/evaluate_models.py
python ranking/material_ranking.py

📤 Outputs
Output	Description
cost_model.pkl	Trained cost model
co2_model.pkl	Trained CO₂ model
RMSE, MAE, R²	Model performance
Ranked materials	Final recommendations
📈 Best Practices

Use separate models for cost & CO₂

Fix random seeds for reproducibility

Save trained models for reuse

Avoid data leakage from test set
