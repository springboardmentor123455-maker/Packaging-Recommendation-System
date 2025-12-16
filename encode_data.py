import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:venky5678@localhost/eco_packaging"
)

with engine.connect() as conn:
    print(" MySQL connection working")


df = pd.read_sql("SELECT * FROM ec_friendly_materials_200_rows", engine)

df_encoded = pd.get_dummies(df, columns=['strength', 'weight_capacity'])

print("Encoded Columns:")
print(df_encoded.head())
