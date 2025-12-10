\c eco_packaging;


DROP TABLE IF EXISTS product_material CASCADE;
DROP TABLE IF EXISTS products_processed CASCADE;
DROP TABLE IF EXISTS materials_processed CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS materials CASCADE;


CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_name VARCHAR(150) NOT NULL UNIQUE,
    material_type VARCHAR(100),

    durability_score INT CHECK (durability_score BETWEEN 0 AND 10),
    cushioning_score INT CHECK (cushioning_score BETWEEN 0 AND 10),
    water_resistance_score INT CHECK (water_resistance_score BETWEEN 0 AND 10),

    
    biodegradability_score INT CHECK (biodegradability_score BETWEEN 0 AND 100),
    recyclability_score INT CHECK (recyclability_score BETWEEN 0 AND 100),

    co2_emission_per_kg DECIMAL(10,2),
    cost_per_kg DECIMAL(10,2),
    weight_capacity_kg DECIMAL(10,2)
);


CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL UNIQUE,

    industry VARCHAR(100),
    weight_kg DECIMAL(10,2),
    volume_cm3 DECIMAL(10,2),

    fragility_level VARCHAR(50),
    moisture_sensitivity VARCHAR(50),
    temperature_sensitivity VARCHAR(50),
    price_usd DECIMAL(10,2)
);


CREATE TABLE product_material (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    material_id INT REFERENCES materials(material_id) ON DELETE CASCADE,
    suitability_score DECIMAL(10,2)
);


CREATE TABLE materials_processed AS TABLE materials WITH NO DATA;
CREATE TABLE products_processed AS TABLE products WITH NO DATA;


CREATE INDEX idx_material_name ON materials(material_name);
CREATE INDEX idx_product_name ON products(product_name);
CREATE INDEX idx_industry ON products(industry);

SELECT 'Schema creation complete.' AS status;
