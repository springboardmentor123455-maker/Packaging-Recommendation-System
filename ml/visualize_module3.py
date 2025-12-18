import pandas as pd
import matplotlib.pyplot as plt
import os

# Create graphs directory if it doesn't exist
os.makedirs("ml/graphs", exist_ok=True)

print("Loading data for visualization...")

# Load datasets
features = pd.read_csv("ml/features.csv")
target_cost = pd.read_csv("ml/target_cost.csv")
target_co2 = pd.read_csv("ml/target_co2.csv")

X_train = pd.read_csv("ml/X_train.csv")
X_train_scaled = pd.read_csv("ml/X_train_scaled.csv")

print("Data loaded successfully")

# -------------------------------
# Graph 1: Feature Distribution
# -------------------------------
plt.figure()
features.hist(figsize=(10, 8))
plt.suptitle("Feature Distribution (Before Scaling)")
plt.tight_layout()
plt.savefig("ml/graphs/feature_distribution.png")
plt.close()

print("Feature distribution graph saved")

# -------------------------------
# Graph 2: Target Distribution
# -------------------------------
plt.figure()
plt.hist(target_cost.iloc[:, 0], bins=20)
plt.title("Cost Target Distribution")
plt.xlabel("Cost Value")
plt.ylabel("Frequency")
plt.savefig("ml/graphs/target_cost_distribution.png")
plt.close()

plt.figure()
plt.hist(target_co2.iloc[:, 0], bins=20)
plt.title("CO₂ Impact Target Distribution")
plt.xlabel("CO₂ Impact Value")
plt.ylabel("Frequency")
plt.savefig("ml/graphs/target_co2_distribution.png")
plt.close()

print("Target distribution graphs saved")

# -------------------------------
# Graph 3: Before vs After Scaling
# -------------------------------
plt.figure()
plt.plot(X_train.iloc[:, 0], label="Before Scaling")
plt.plot(X_train_scaled.iloc[:, 0], label="After Scaling")
plt.legend()
plt.title("Before vs After Feature Scaling")
plt.savefig("ml/graphs/scaling_comparison.png")
plt.close()

print("Scaling comparison graph saved")

print("Module 3 visualization completed successfully")
