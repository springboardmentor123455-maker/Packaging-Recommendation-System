import pandas as pd
from sqlalchemy import create_engine

print("Starting data cleaning...")

engine = create_engine(
    "mysql+pymysql://root:venky5678@localhost/eco_packaging"
)

df = pd.read_sql("SELECT * FROM materials", engine)

print("Before cleaning:")
print(df.isnull().sum())

df['biodegradability_score'] = df['biodegradability_score'].fillna(
    df['biodegradability_score'].mean()
)
df['co2_emission_score'] = df['co2_emission_score'].fillna(
    df['co2_emission_score'].mean()
)
df['recyclability_percent'] = df['recyclability_percent'].fillna(
    df['recyclability_percent'].mean()
)

print("\nAfter cleaning:")
print(df.isnull().sum())

print("\n✅ Data cleaning completed")
