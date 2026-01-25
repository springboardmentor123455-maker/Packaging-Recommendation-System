
---

# ✅ 2) Technical Documentation (Paste in `DOCUMENTATION.md` OR in README)

```md
# Technical Documentation – Packaging Recommendation System

## 1. Overview
This project is a Flask-based web application that recommends packaging materials using a weighted scoring model.  
The system stores materials, products, and recommendations in a PostgreSQL database.

## 2. System Architecture
- **Frontend (HTML/CSS/JS)**: Used for product input, recommendations display, and dashboard charts.
- **Backend (Flask API)**: Provides endpoints for CRUD + recommendation logic + dashboard calculations.
- **Database (PostgreSQL)**: Stores `Material`, `Product`, and `Recommendation`.

## 3. Database Design (Models)

### Material Table
Stores packaging material features:
- material_name
- material_type
- recyclable
- biodegradable
- density
- strength
- cost_per_kg
- co2_per_kg

### Product Table
Stores product input data:
- product_name
- category
- weight_kg
- fragile
- shipping_distance_km
- created_at

### Recommendation Table
Stores recommendations for each product:
- product_id (FK)
- material_name
- final_score
- estimated_cost
- estimated_co2
- created_at

## 4. Recommendation Algorithm
For each material:
- Convert cost and CO₂ to inverse scores
- Add bonus for recyclable & fragile protection
- Add category bonus based on product type
- Sort by `final_score` and return top 5

## 5. Dashboard Calculations
Dashboard computes:
- total products
- total recommendations
- top materials used
- baseline cost and CO₂
- recommended cost and CO₂
- savings % and CO₂ reduction %

## 6. Deployment
Deployed using Render Web Service with:
- `gunicorn app:app`
- PostgreSQL cloud database linked via environment variable `DB_URL`

## 7. Environment Variables
Required environment variable:
- `DB_URL` → Full PostgreSQL connection URL from Render Database

## 8. Run-time Initialization
After deployment, database tables are created via:
- `/init-db` endpoint

## 9. Limitations
- Baseline cost/CO₂ are assumed constants for estimation
- Requires adding sample materials before recommendation results appear

## 10. Future Improvements
- Add authentication
- Add Admin panel for materials management
- Improve scoring model using ML / training data
- Add chart filters and export options
