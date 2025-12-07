-- EcoPackAI Week 1 database schema
-- Author: Lokesh Patil (Springboard_01)

CREATE TABLE IF NOT EXISTS materials (
    material_id SERIAL PRIMARY KEY,
    material_name          VARCHAR(150) NOT NULL,
    category               VARCHAR(50),
    strength_mpa           NUMERIC(10,2),
    weight_capacity_kg     NUMERIC(10,2),
    biodegradability_score NUMERIC(5,2) CHECK (biodegradability_score BETWEEN 0 AND 100),
    co2_emission_score     NUMERIC(10,3),
    recyclability_percent  NUMERIC(5,2) CHECK (recyclability_percent BETWEEN 0 AND 100),
    cost_per_kg            NUMERIC(10,2) NOT NULL,
    created_at             TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS materials_staging (
    material_name          VARCHAR(150),
    category               VARCHAR(50),
    strength_mpa           NUMERIC(10,2),
    weight_capacity_kg     NUMERIC(10,2),
    biodegradability_score NUMERIC(5,2),
    co2_emission_score     NUMERIC(10,3),
    recyclability_percent  NUMERIC(5,2),
    cost_per_kg            NUMERIC(10,2)
);
