CREATE TABLE Materials (
    Material_ID SERIAL PRIMARY KEY,
    Material_Type VARCHAR(50),
    Strength NUMERIC,
    Weight_Capacity NUMERIC,
    Biodegradability_Score NUMERIC,
    CO2_Emission_Score NUMERIC,
    Recyclability_Percent NUMERIC
);
