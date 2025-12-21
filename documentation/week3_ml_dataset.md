## Week 3 – ML Dataset Preparation (Lokesh Patil – Springboard_01)

### Objective
Prepare a machine-learning-ready dataset from the cleaned data generated in Module 2.

---

### Input Dataset
- Source: `data/materials_cleaned.csv`
- Contains engineered features such as CO₂ impact index, cost efficiency index, and suitability score.

---

### Feature Selection
**Input Features (X):**
- strength_mpa  
- weight_capacity_kg  
- biodegradability_score  
- recyclability_percent  
- category (one-hot encoded)

**Target Variables (y):**
- `cost_per_kg` → Cost prediction  
- `co2_impact_index` → CO₂ impact prediction  

---

### Categorical Encoding
- Applied **One-Hot Encoding** to the `category` column using `pandas.get_dummies`.
- Converted categorical material types into numeric form suitable for ML models.

---

### Train–Test Split
- Split ratio: **80% training / 20% testing**
- Random seed: `random_state = 42`
- Separate splits created for cost and CO₂ targets.

---

### Output Files Generated
- `X_train.csv`
- `X_test.csv`
- `y_cost_train.csv`
- `y_cost_test.csv`
- `y_co2_train.csv`
- `y_co2_test.csv`

---

### Week 3 Status
✔ ML dataset preparation completed  
✔ Ready for Week 4 – Model training and evaluation
