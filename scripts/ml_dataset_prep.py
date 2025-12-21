# scripts/ml_dataset_prep.py
"""
Week 3: Machine Learning Dataset Preparation
Prepares train-test datasets for cost and CO2 prediction models.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_CSV = os.path.join(ROOT, "data", "materials_cleaned.csv")
OUTPUT_DIR = os.path.join(ROOT, "data")

def main():
    # 1. Load cleaned data
    df = pd.read_csv(INPUT_CSV)
    print("Loaded rows:", len(df))

    # 2. Select input features (X)
    X = df[
        [
            "strength_mpa",
            "weight_capacity_kg",
            "biodegradability_score",
            "recyclability_percent",
            "category",
        ]
    ]

    # 3. Encode categorical column (category)
    X = pd.get_dummies(X, columns=["category"], drop_first=True)

    # 4. Define target variables (y)
    y_cost = df["cost_per_kg"]
    y_co2 = df["co2_impact_index"]

    # 5. Train-test split (80% train, 20% test)
    X_train, X_test, y_cost_train, y_cost_test = train_test_split(
        X, y_cost, test_size=0.2, random_state=42
    )

    _, _, y_co2_train, y_co2_test = train_test_split(
        X, y_co2, test_size=0.2, random_state=42
    )

    # 6. Save datasets
    X_train.to_csv(os.path.join(OUTPUT_DIR, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(OUTPUT_DIR, "X_test.csv"), index=False)

    y_cost_train.to_csv(os.path.join(OUTPUT_DIR, "y_cost_train.csv"), index=False)
    y_cost_test.to_csv(os.path.join(OUTPUT_DIR, "y_cost_test.csv"), index=False)

    y_co2_train.to_csv(os.path.join(OUTPUT_DIR, "y_co2_train.csv"), index=False)
    y_co2_test.to_csv(os.path.join(OUTPUT_DIR, "y_co2_test.csv"), index=False)

    print("ML datasets created successfully")

if __name__ == "__main__":
    main()
