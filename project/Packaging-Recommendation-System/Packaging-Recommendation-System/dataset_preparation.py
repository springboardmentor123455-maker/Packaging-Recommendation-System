#  MODULE 3: MACHINE LEARNING DATASET PREPARATION
#  Train–Test Split Code
'''Module 3: Machine Learning Dataset Preparation
✔ Load dataset
✔ Select features & target
✔ Train/Test split
✔ Save processed datasets'''
# ============================================================

import pandas as pd
from sklearn.model_selection import train_test_split

# 1. LOAD THE FINAL DATASET (USE THE FEATURE-ENGINEERED ONE)
df = pd.read_csv("fully_featured_materials.csv")
print("Rows loaded:", len(df))
print("Columns:", df.columns.tolist())


# 2. SELECT FEATURES & TARGET
# Dropping ID + target column from features
X = df.drop(columns=["material_id", "material_suitability_score"])

# Target column
y = df["material_suitability_score"]

print("\nFeature count:", X.shape[1])
print("Target:", "material_suitability_score")

# 3. SPLIT INTO TRAIN & TEST SETS
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.2,      # 80% training, 20% testing
    random_state=42,    # makes split reproducible
    shuffle=True
)

print("\nTrain/Test Split Completed!")
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)


# 4. SAVE OUTPUT FILES
X_train.to_csv("data/X_train.csv", index=False)
X_test.to_csv("data/X_test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

print("\nSaved split datasets into /data folder!")



# ---------------------------
# CHOOSE YOUR TARGET COLUMN
# ---------------------------

# Option 1: Predict material safety
# target_col = "material_safety_score"

# Option 2: Predict strength
target_col = "strength_MPa"

# Option 3: Predict shipping category
# target_col = "shipping_category"

# ⚠️ SELECT YOUR TARGET HERE
#target_col = "material_suitability_score"   # example

# ---------------------------
# FEATURE SELECTION
# ---------------------------

# Drop ID + Target from features
X = df.drop(columns=["material_id", target_col])

# Target
y = df[target_col]

print("Selected Target:", target_col)
print("X shape:", X.shape)
print("y shape:", y.shape)

# ---------------------------
# TRAIN–TEST SPLIT
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTrain/Test Split Completed!")
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)