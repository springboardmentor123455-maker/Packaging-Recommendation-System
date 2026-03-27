CREATE TABLE Products (
    Product_ID SERIAL PRIMARY KEY,
    Product_Name VARCHAR(100),
  
    Industry_Category VARCHAR(50),
    Packaging_Type VARCHAR(50),
  
    Transport_Distance NUMERIC,
    Transport_Mode VARCHAR(50),
    Delivery_Carbon NUMERIC,
  
    Energy_Consumption NUMERIC,
    Water_Usage NUMERIC,
    Waste_Generated NUMERIC
);
