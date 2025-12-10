import pandas as pd

def simple_recommendation():
    # Read cleaned materials data
    df = pd.read_csv("data/materials_cleaned.csv")

    print("\n=== Simple Material Recommendation Demo ===\n")
    print("Showing first 3 materials from cleaned data:")
    print(df.head(3))

    # Example: select the most eco-friendly material
    best_material = df.sort_values(by="recyclability_percent", ascending=False).iloc[0]

    print("\nBest Eco-Friendly Material Recommendation:")
    print(best_material)

if __name__ == "__main__":
    simple_recommendation()