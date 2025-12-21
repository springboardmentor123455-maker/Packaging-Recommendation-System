# 📦 EcoPackAI  
## Module 3: Machine Learning Dataset Preparation  
(Train–Test Split, Scaling & ML-Ready Pipelines)

---

## 📌 Module Overview

Module 3 prepares the feature-engineered dataset from Module 2 for machine learning model training.  
It ensures the dataset is properly split, scaled, and structured into features and targets.

---

## 🎯 Objectives

- Load feature-engineered dataset  
- Select relevant ML features  
- Define target variables:
  - Cost Prediction
  - CO₂ Impact Prediction
- Perform train–test split  
- Apply feature scaling  
- Save ML-ready datasets  

---

## 🔄 Input & Output

### Input
- engineered_features.csv (from Module 2)

### Output
- X_train.csv  
- X_test.csv  
- y_cost_train.csv  
- y_cost_test.csv  
- y_co2_train.csv  
- y_co2_test.csv  

---

## 🗂 Folder Structure

```
EcoPackAI/
└── module3_ml_dataset/
    ├── data/
    │   └── engineered_features.csv
    ├── pipeline/
    │   ├── feature_selection.py
    │   ├── split_data.py
    │   └── scale_data.py
    ├── outputs/
    │   ├── X_train.csv
    │   ├── X_test.csv
    │   ├── y_cost_train.csv
    │   ├── y_cost_test.csv
    │   ├── y_co2_train.csv
    │   └── y_co2_test.csv
    └── README.md
```

---

## 🛠 Packages Used

| Package | Version |
|------|--------|
| python | 3.10 |
| pandas | 2.1.1 |
| numpy | 1.26.2 |
| scikit-learn | 1.3.2 |

---

## ⚙️ Installation

```bash
pip install pandas==2.1.1 numpy==1.26.2 scikit-learn==1.3.2
```

---

## 🧠 Step 1: Feature Selection

File: feature_selection.py

```python
import pandas as pd

def select_features(file_path):
    df = pd.read_csv(file_path)

    X = df[
        [
            "strength_rating",
            "weight_capacity_kg",
            "biodegradability_score",
            "recyclability_percent",
            "co2_impact_index",
            "cost_efficiency_index",
            "material_type_encoded"
        ]
    ]

    y_cost = df["cost_per_unit"]
    y_co2 = df["co2_emission_score"]

    return X, y_cost, y_co2
```

---

## ✂️ Step 2: Train–Test Split

File: split_data.py

```python
from sklearn.model_selection import train_test_split

def split_dataset(X, y_cost, y_co2, test_size=0.2):
    X_train, X_test, y_cost_train, y_cost_test = train_test_split(
        X, y_cost, test_size=test_size, random_state=42
    )

    _, _, y_co2_train, y_co2_test = train_test_split(
        X, y_co2, test_size=test_size, random_state=42
    )

    return X_train, X_test, y_cost_train, y_cost_test, y_co2_train, y_co2_test
```

---

## ⚖️ Step 3: Feature Scaling

File: scale_data.py

```python
from sklearn.preprocessing import StandardScaler
import pandas as pd

def scale_features(X_train, X_test):
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    return X_train_scaled, X_test_scaled
```

---

## ▶️ How to Run Module 3

```bash
python pipeline/feature_selection.py
python pipeline/split_data.py
python pipeline/scale_data.py
```

---

## 📤 Outputs

| File | Description |
|----|------------|
| X_train.csv | Training features |
| X_test.csv | Testing features |
| y_cost_train.csv | Cost target (train) |
| y_cost_test.csv | Cost target (test) |
| y_co2_train.csv | CO₂ target (train) |
| y_co2_test.csv | CO₂ target (test) |

---

## 📈 Best Practices

- Use fixed random_state for reproducibility  
- Scale features after train–test split  
- Save intermediate outputs  

---

## 🔗 Dependency

Output of this module is used by:
➡ Module 4: AI Recommendation Model

---

## ✅ Module 3 Status

✔ Features selected  
✔ Dataset split  
✔ Scaled ML-ready data generated  
