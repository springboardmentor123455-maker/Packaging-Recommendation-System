import psycopg2
import pandas as pd

connection = psycopg2.connect(
    host="localhost",
    database="ecopackai",
    user="postgres",
    password="postgres"
)

query = "SELECT * FROM materials;"
df = pd.read_sql(query, connection)

connection.close()

print(df.head())
print(df.shape)
#checking missing values/
print(df.isnull().sum())

df.rename(columns={
    'material_type': 'material_type',
    'strength_mpa': 'strength',
    'weight_capacity_kg': 'weight_capacity',
    'biodegradability_score': 'biodegradability',
    'co2_emission_score': 'co2_emission',
    'recyclability_percent': 'recyclability'
}, inplace=True)

df = pd.get_dummies(df, columns=['material_type'], drop_first=True)
#save clean 
df.to_csv("clean_materials.csv", index=False)
