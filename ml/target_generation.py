import pandas as pd

df = pd.read_csv("data/processed_materials.csv")

y_cost = df[['cost_efficiency_index']]
y_co2 = df[['co2_impact_index']]

y_cost.to_csv("ml/target_cost.csv", index=False)
y_co2.to_csv("ml/target_co2.csv", index=False)

print("✅ Target generation completed")
