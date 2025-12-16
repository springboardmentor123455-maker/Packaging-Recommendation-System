import pandas as pd
from sklearn.model_selection import train_test_split
import os

# ==============================
# STEP 1: DEFINE DATA FOLDER
# ==============================
DATA_FOLDER = "data"

FEATURE_FILE = os.path.join(DATA_FOLDER, "feature_engineered_materials.csv")

print("📁 Using data folder:", DATA_FOLDER)
print("📄 Looking for:", FEATURE_FILE)

# ==============================
# STEP 2: CHECK FILE EXISTS
# ==============================
if not os.path.exists(FEATURE_FILE):
    raise FileNotFoundError(
        f"\n❌ feature_engineered_materials.csv NOT FOUND\n"
        f"Expected location: {FEATURE_FILE}\n"
        "➡ Please run Day 5 first."
    )

# ==============================
# STEP 3: LOAD DATA
# ==============================
df = pd.read_csv(FEATURE_FILE)
print("✔ Dataset loaded:", df.shape)

# ==============================
# STEP 4: DEFINE FEATURES & TARGETS
# ==============================
X = df.drop(columns=[
    "material_suitability_score",
    "rank"
])

y_co2 = df["co2_impact_index"]
y_suitability = df["material_suitability_score"]

# ==============================
# STEP 5: TRAIN–TEST SPLIT
# ==============================
X_train, X_test, y_co2_train, y_co2_test = train_test_split(
    X,
    y_co2,
    test_size=0.2,
    random_state=42
)

_, _, y_suit_train, y_suit_test = train_test_split(
    X,
    y_suitability,
    test_size=0.2,
    random_state=42
)

# ==============================
# STEP 6: SAVE ALL FILES INTO data/
# ==============================
X_train.to_csv(os.path.join(DATA_FOLDER, "X_train.csv"), index=False)
X_test.to_csv(os.path.join(DATA_FOLDER, "X_test.csv"), index=False)

y_co2_train.to_csv(os.path.join(DATA_FOLDER, "y_co2_train.csv"), index=False)
y_co2_test.to_csv(os.path.join(DATA_FOLDER, "y_co2_test.csv"), index=False)

y_suit_train.to_csv(os.path.join(DATA_FOLDER, "y_suitability_train.csv"), index=False)
y_suit_test.to_csv(os.path.join(DATA_FOLDER, "y_suitability_test.csv"), index=False)

print("\n🎉 DAY 6 COMPLETED SUCCESSFULLY")
print("📦 All ML datasets saved inside data/ folder")
