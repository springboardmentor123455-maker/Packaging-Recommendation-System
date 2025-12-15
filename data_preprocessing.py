import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler

# MySQL connection
engine = create_engine(
    "mysql+pymysql://root:venky5678@localhost/eco_packaging"
)

query = "SELECT * FROM ec_friendly_materials_200_rows"

df = pd.read_sql(query, engine)

print("Data loaded from MySQL")
print(df.head())

# Handle missing values
df['biodegradability_score'].fillna(df['biodegradability_score'].mean(), inplace=True)
df['co2_emission_score'].fillna(df['co2_emission_score'].mean(), inplace=True)
df['recyclability_percent'].fillna(df['recyclability_percent'].mean(), inplace=True)


scaler = MinMaxScaler()

df[['biodegradability_score',
    'co2_emission_score',
    'recyclability_percent']] = scaler.fit_transform(
        df[['biodegradability_score',
            'co2_emission_score',
            'recyclability_percent']]
)


df = pd.get_dummies(
    df,
    columns=['material_type', 'strength', 'weight_capacity'],
    drop_first=True
)


df['co2_impact_index'] = 1 - df['co2_emission_score']


df['co2_impact_index'] = 1 - df['co2_emission_score']


df['cost_efficiency_index'] = (
    df['biodegradability_score'] +
    df['recyclability_percent']
) / 2


df['material_suitability_score'] = (
    df['biodegradability_score'] * 0.4 +
    df['recyclability_percent'] * 0.4 +
    df['co2_impact_index'] * 0.2
)


print(df.describe())


df.to_csv("data/processed_materials.csv", index=False)
print("Processed data saved successfully")


