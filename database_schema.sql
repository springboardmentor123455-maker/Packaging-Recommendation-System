-- EcoPackAI Database Schema
-- PostgreSQL database structure for sustainable packaging recommendation system

-- Drop existing tables if they exist
DROP TABLE IF EXISTS packaging_recommendations CASCADE;
DROP TABLE IF EXISTS materials_data CASCADE;
DROP TABLE IF EXISTS product_categories CASCADE;

-- Create materials_data table
CREATE TABLE materials_data (
    material_id SERIAL PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    material_type VARCHAR(100) NOT NULL,
    strength DECIMAL(10, 2) NOT NULL,  -- kg/cm²
    weight_capacity DECIMAL(10, 2) NOT NULL,  -- kg
    biodegradability_score DECIMAL(5, 2) CHECK (biodegradability_score >= 0 AND biodegradability_score <= 100),
    co2_emission_score DECIMAL(10, 3) NOT NULL,  -- kg CO₂/kg material
    recyclability_percent DECIMAL(5, 2) CHECK (recyclability_percent >= 0 AND recyclability_percent <= 100),
    cost_per_kg DECIMAL(10, 2) NOT NULL,  -- USD
    thickness_mm DECIMAL(10, 2),
    water_resistance INTEGER CHECK (water_resistance >= 1 AND water_resistance <= 10),
    temperature_tolerance INTEGER,  -- °C
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create product_categories table
CREATE TABLE product_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    fragility_level INTEGER CHECK (fragility_level >= 1 AND fragility_level <= 10),
    required_strength DECIMAL(10, 2) NOT NULL,
    moisture_sensitivity INTEGER CHECK (moisture_sensitivity >= 1 AND moisture_sensitivity <= 10),
    temperature_sensitivity INTEGER CHECK (temperature_sensitivity >= 1 AND temperature_sensitivity <= 10),
    typical_weight_min DECIMAL(10, 2),
    typical_weight_max DECIMAL(10, 2),
    recommended_materials TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create packaging_recommendations table (for ML predictions)
CREATE TABLE packaging_recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    material_id INTEGER REFERENCES materials_data(material_id),
    category_id INTEGER REFERENCES product_categories(category_id),
    suitability_score DECIMAL(5, 2),
    predicted_cost DECIMAL(10, 2),
    predicted_co2_impact DECIMAL(10, 3),
    recommendation_rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance optimization
CREATE INDEX idx_material_type ON materials_data(material_type);
CREATE INDEX idx_biodegradability ON materials_data(biodegradability_score DESC);
CREATE INDEX idx_recyclability ON materials_data(recyclability_percent DESC);
CREATE INDEX idx_co2_emission ON materials_data(co2_emission_score ASC);
CREATE INDEX idx_category_name ON product_categories(category_name);
CREATE INDEX idx_recommendation_score ON packaging_recommendations(suitability_score DESC);

-- Create views for analytics
CREATE OR REPLACE VIEW high_sustainability_materials AS
SELECT 
    material_id,
    material_name,
    material_type,
    biodegradability_score,
    recyclability_percent,
    co2_emission_score,
    cost_per_kg
FROM materials_data
WHERE biodegradability_score > 70 
  AND recyclability_percent > 60
  AND co2_emission_score < 2.0
ORDER BY biodegradability_score DESC;

CREATE OR REPLACE VIEW cost_efficient_materials AS
SELECT 
    material_id,
    material_name,
    material_type,
    strength,
    cost_per_kg,
    (strength / cost_per_kg) AS strength_cost_ratio
FROM materials_data
ORDER BY strength_cost_ratio DESC;

-- Summary statistics view
CREATE OR REPLACE VIEW material_statistics AS
SELECT 
    material_type,
    COUNT(*) as count,
    AVG(strength) as avg_strength,
    AVG(biodegradability_score) as avg_biodegradability,
    AVG(co2_emission_score) as avg_co2,
    AVG(recyclability_percent) as avg_recyclability,
    AVG(cost_per_kg) as avg_cost
FROM materials_data
GROUP BY material_type
ORDER BY avg_biodegradability DESC;

-- Comments for documentation
COMMENT ON TABLE materials_data IS 'Stores comprehensive data about eco-friendly packaging materials';
COMMENT ON TABLE product_categories IS 'Defines product categories with specific packaging requirements';
COMMENT ON TABLE packaging_recommendations IS 'Stores ML-based recommendations for optimal packaging';

COMMENT ON COLUMN materials_data.strength IS 'Material strength in kg/cm²';
COMMENT ON COLUMN materials_data.biodegradability_score IS 'Biodegradability rating from 0-100 (higher is better)';
COMMENT ON COLUMN materials_data.co2_emission_score IS 'CO₂ emissions per kg of material (lower is better)';
COMMENT ON COLUMN materials_data.recyclability_percent IS 'Percentage of material that can be recycled';
