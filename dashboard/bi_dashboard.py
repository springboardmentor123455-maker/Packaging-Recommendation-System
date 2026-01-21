# bi_dashboard.py
# Module 7: Business Intelligence Dashboard

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Ensure folders exist
# -------------------------------
os.makedirs("dashboard/charts", exist_ok=True)
os.makedirs("reports", exist_ok=True)

print("\n==== BUSINESS INTELLIGENCE DASHBOARD ====\n")

# -------------------------------
# Sample sustainability data
# -------------------------------
data = pd.DataFrame({
    "material": [
        "Cardboard", "Bioplastic", "Molded Pulp",
        "Paper Foam", "Corrugated Fiber", "Bagasse"
    ],
    "original_co2": [80, 95, 70, 85, 90, 88],
    "predicted_co2": [50, 55, 40, 60, 58, 52],
    "original_cost": [120, 160, 110, 140, 150, 145],
    "predicted_cost": [90, 115, 85, 100, 105, 98]
})

print("Data Loaded Successfully\n")
print(data)

# -------------------------------
# Calculations
# -------------------------------
data["co2_reduction_percent"] = (
    (data["original_co2"] - data["predicted_co2"])
    / data["original_co2"]
) * 100

data["cost_savings"] = data["original_cost"] - data["predicted_cost"]

print("\nCalculated Sustainability Metrics\n")
print(data[["material", "co2_reduction_percent", "cost_savings"]])

# -------------------------------
# CO₂ Reduction Chart
# -------------------------------
plt.figure()
plt.bar(data["material"], data["co2_reduction_percent"])
plt.title("CO₂ Reduction Percentage by Material")
plt.ylabel("Reduction (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("dashboard/charts/co2_reduction.png")
plt.close()

# -------------------------------
# Cost Savings Chart
# -------------------------------
plt.figure()
plt.bar(data["material"], data["cost_savings"])
plt.title("Cost Savings by Material")
plt.ylabel("Amount Saved")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("dashboard/charts/cost_savings.png")
plt.close()

print("\nCharts Generated Successfully")
print("✔ CO₂ Reduction Chart")
print("✔ Cost Savings Chart")

# -------------------------------
# Save data for report generation
# -------------------------------
data.to_csv("reports/sustainability_data.csv", index=False)

print("\nDashboard processing completed successfully!\n")
