import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

X_train = pd.read_csv("ml/X_train.csv")
X_test = pd.read_csv("ml/X_test.csv")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pd.DataFrame(X_train_scaled).to_csv("ml/X_train_scaled.csv", index=False)
pd.DataFrame(X_test_scaled).to_csv("ml/X_test_scaled.csv", index=False)

joblib.dump(scaler, "ml/scaler.pkl")

print("✅ Scaling and pipeline preparation completed")
