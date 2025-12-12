Module 1 — Data Collection & Management

Milestone: Week 1–2
Project: EcoPackAI – AI-Powered Sustainable Packaging Recommendation System


---

1. Objective

Establish a complete material and product dataset required for the AI recommendation system.
This module focuses on:

Collecting eco-friendly packaging material data

Creating a structured material dataset (CSV + database)

Designing PostgreSQL tables

Ensuring schema validation for clean and consistent data



---

2. Material Dataset Requirements

Each material should include the following attributes:

Attribute	Description

material_id	Unique identifier
material_name	Name of material (e.g., Kraft Paper)
material_type	Category (Paper, Plastic, Textile, etc.)
strength_kg	Load strength
weight_r_per_m2	Weight per unit area
biodegradability_score	Range: 0–1
co2_emission_kg_per_kg	CO₂ footprint per kg
recyclability_percent	Percentage recyclable
cost_per_kg	Price of material
water_resistance_score	Range: 0–1
other_notes	Optional metadata



---

3. Sample Raw Dataset (materials.csv)

material_id,material_name,material_type,strength_kg,weight_r_per_m2,biodegradability_score,co2_emission_kg_per_kg,recyclability_percent,cost_per_kg,water_resistance_score,other_notes
1,Kraft_Paper,Paper,120,190,0.9,0.7,80,0.12,0.3,uses:boxes
2,Corrugated_Carton,Paper,300,200,0.85,0.9,70,0.20,0.4,shipping
3,Molded_Pulp,Pulp,200,350,0.95,0.4,90,0.08,0.2,fragile packaging


---

4. PostgreSQL Database Schema

Table: materials

CREATE TABLE materials (
  material_id SERIAL PRIMARY KEY,
  material_name TEXT NOT NULL,
  material_type TEXT,
  strength_kg NUMERIC,
  weight_r_per_m2 NUMERIC,
  biodegradability_score NUMERIC,
  co2_emission_kg_per_kg NUMERIC,
  recyclability_percent NUMERIC,
  cost_per_kg NUMERIC,
  water_resistance_score NUMERIC,
  other_notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);


---

5. Importing CSV into PostgreSQL

psql -d ecopackai -c "\copy materials(material_name, material_type, strength_kg, weight_r_per_m2, biodegradability_score, co2_emission_kg_per_kg, recyclability_percent, cost_per_kg, water_resistance_score, other_notes) FROM 'data/materials.csv' CSV HEADER;"


---

6. Data Management Best Practices

Store raw dataset in data/materials.csv

Do NOT modify raw file; generate a cleaned version in Module 2

Ensure consistent column names and units

Maintain a Data Dictionary inside this documentation folder



---

7. Module 1 Output Deliverables

✔ materials.csv (raw dataset)
✔ PostgreSQL table materials created
✔ Schema validated
✔ Code and screenshots added to GitHub


---