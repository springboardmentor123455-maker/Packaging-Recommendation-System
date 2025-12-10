## Module 2 – Data Cleaning & Feature Engineering (Lokesh Patil – Springboard_01)

### 1. Raw Data Overview
- Source: `data/materials_raw.csv`
- Contains 10 eco-friendly packaging materials with mechanical and environmental properties.

### 2. Data Cleaning Steps
- Converted numeric types using `pd.to_numeric(errors='coerce')`.
- Trimmed whitespace in categorical fields.
- Dropped duplicates.
- Filled missing values in numeric columns using **median imputation**.
- Confirmed zero NULL values in critical columns.

### 3. Feature Normalization
Applied **Min–Max Scaling** to:
- strength_mpa  
- weight_capacity_kg  
- biodegradability_score  
- co2_emission_score  
- recyclability_percent  
- cost_per_kg  

Purpose: normalize features to 0–1 so differing units don't bias the composite scores.

### 4. Feature Engineering

#### CO₂ Impact Index

Interprets environmental burden (lower is better).

#### Cost Efficiency Index

Balances low cost with recyclability (higher is better).

#### Material Suitability Score

Composite score used to rank materials for recommendations.

### 5. Ranking & Output
- Sorted by `material_suitability_score` (descending) and added `rank`.
- Exported cleaned data to `data/materials_cleaned.csv`.
- Uploaded cleaned table to PostgreSQL as `materials_cleaned`.
- Script used: `scripts/data_cleaning.py`
- DB connection via `.env` (PG_CONN), not committed.

### 6. Validation & Quality Checks
Performed the following checks (examples):
- `SELECT COUNT(*) FROM materials_cleaned;` → total rows = 10
- Null checks for key fields → 0 rows
- Out-of-range checks for percent fields → 0 rows
- Min/Max/Avg checks for cost and scores to ensure realistic values

### 7. Deliverables (on branch `Springboard_01`)
- `scripts/data_cleaning.py` (script)
- `data/materials_cleaned.csv` (cleaned dataset)
- `database/create_db.sql` (schema)
- `documentation/week2_progress.md` (this file)
- `.env` kept local (ignored by git)

### 8. Status
✔ Module-2 completed and validated.  
✔ Ready to proceed to Module-3 (EDA & Visualization).

