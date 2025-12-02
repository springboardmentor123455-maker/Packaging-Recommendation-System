import pandas as pd

# Load the materials data
def load_data():
    df = pd.read_csv("data/materials.csv")
    return df

# Simple cleaning for Week-1
def clean_data(df):
    # Fill missing numerical values with median
    df = df.fillna(df.median(numeric_only=True))
    return df

# Save cleaned file
def save_cleaned(df):
    df.to_csv("data/materials_cleaned.csv", index=False)
    print("Cleaned data saved to data/materials_cleaned.csv")

if __name__ == "__main__":
    df = load_data()
    cleaned_df = clean_data(df)
    save_cleaned(cleaned_df)
    print(cleaned_df.head())
