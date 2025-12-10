CREATE TABLE packaging_materials (
    id SERIAL PRIMARY KEY,
    material_name VARCHAR(150) NOT NULL,
    material_type VARCHAR(100),
    
   
    tensile_strength FLOAT,          
    weight_capacity FLOAT,           
    
   
    biodegradability_score INT,      
    co2_emission_score FLOAT,        
    recyclability_percent INT,       
    
   
    price_inr_per_unit FLOAT,
    suitable_industries TEXT         
);