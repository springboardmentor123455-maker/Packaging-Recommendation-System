-- EcoPackAI Project
-- Week 1: Materials Table Schema

-- Create database (optional, for documentation)
-- CREATE DATABASE ecopackai;

-- Drop table if it exists
DROP TABLE IF EXISTS materials;

-- Create materials table
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR(100),
    strength_mpa FLOAT,
    weight_capacity_kg FLOAT,
    biodegradability_score FLOAT,
    co2_emission_score FLOAT,
    recyclability_percent FLOAT
);
