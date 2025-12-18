import pandas as pd
from sklearn.model_selection import train_test_split

X = pd.read_csv("ml/features.csv")
y_cost = pd.read_csv("ml/target_cost.csv")
y_co2 = pd.read_csv("ml/target_co2.csv")

X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

_, _, y_co2_train, y_co2_test = train_test_split(
    X, y_co2, test_size=0.2, random_state=42
)

X_train.to_csv("ml/X_train.csv", index=False)
X_test.to_csv("ml/X_test.csv", index=False)

y_cost_train.to_csv("ml/y_cost_train.csv", index=False)
y_cost_test.to_csv("ml/y_cost_test.csv", index=False)

y_co2_train.to_csv("ml/y_co2_train.csv", index=False)
y_co2_test.to_csv("ml/y_co2_test.csv", index=False)

print("✅ Train-test split completed")
