# Week 1 – Data & Database Setup (Lokesh Patil – Springboard_01)

## Database & Tables
- Installed PostgreSQL 18 and pgAdmin 4 locally.
- Created database: `ecopackai_db`.
- Created tables:
  - `materials`
  - `materials_staging`
  using `database/create_db.sql`.

## Dataset
- Prepared `data/materials_raw.csv` with 10 eco-friendly packaging materials.
- Columns:
  - material_name, category, strength_mpa, weight_capacity_kg,
    biodegradability_score, co2_emission_score, recyclability_percent, cost_per_kg.

## Data Loading
- Imported CSV into `materials_staging` using pgAdmin Import (CSV with Header enabled).
- Inserted data from `materials_staging` into final `materials` table using:
  `INSERT INTO materials (...) SELECT ... FROM materials_staging;`.

## Schema & Data Validation
- Verified schema using `information_schema.columns` on the `materials` table.
- Row count in `materials` = 10.
- Null check for `material_name` and `cost_per_kg` = 0 rows.
- All `biodegradability_score` and `recyclability_percent` values are within 0–100.
- Computed min, max and avg for `cost_per_kg` to confirm realistic values.
