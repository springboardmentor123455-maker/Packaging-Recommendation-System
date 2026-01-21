# Packaging-Recommendation-System

https://packaging-recommendation-system.onrender.com/

🌱 EcoPackAI — Sustainable Packaging Recommendation System

EcoPackAI is an AI-powered decision-support system designed to help organizations select optimal packaging materials by balancing environmental sustainability, product safety, and cost efficiency.
The system integrates machine learning, backend APIs, interactive dashboards, and automated sustainability reporting into a single end-to-end platform.

📌 Project Overview

Traditional packaging decisions are often made without considering long-term environmental impact or data-driven cost optimization. EcoPackAI addresses this gap by providing:

AI-based packaging material recommendations

Cost and CO₂ impact prediction

Product-specific material suitability analysis

Business Intelligence dashboards

Exportable sustainability reports (PDF & Excel)

The system enables organizations to move toward data-driven sustainable packaging decisions.

🎯 Key Objectives

Recommend eco-friendly packaging materials using machine learning

Predict packaging cost and environmental impact

Provide product-aware material suitability ranking

Visualize sustainability metrics through dashboards

Enable decision-ready sustainability reports

Deploy a scalable and modular AI system

🧠 System Architecture
EcoPackAI
│
├── data/
│   ├── materials.csv
│   ├── products.csv
│   ├── processed_materials.csv
│   └── product_material_ranking_named.csv
│
├── trained_models/
│   ├── cost_model.pkl
│   ├── co2_model.pkl
│   └── pm_model.pkl
│
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── dashboard.py
│   ├── auth.py
│   └── __init__.py
│
├── static/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
└── README.md

⚙️ Technologies Used
Backend

Python

Flask

Pandas

NumPy

Joblib

ReportLab

OpenPyXL

Machine Learning

Random Forest Regressor (Cost Prediction)

XGBoost Regressor (CO₂ Prediction)

Product–Material Suitability Model

Frontend

HTML5

CSS3

Bootstrap 5

JavaScript (ES6)

Chart.js

Deployment

Render (Cloud Platform)

🧪 Machine Learning Models
Model	Purpose
Cost Prediction Model	Estimates packaging cost
CO₂ Prediction Model	Predicts environmental impact
Suitability Model	Ranks materials per product
Model Performance (Approx.)

Cost Prediction: R² ≈ 0.97

CO₂ Prediction: R² ≈ 0.96

Suitability Prediction: R² ≈ 0.99

🔐 API Security

All protected endpoints require an API key:

x-api-key: ECO2025


Implemented using Flask decorators to prevent unauthorized access.

🔁 Backend API Endpoints
Basic Lookup
Endpoint	Method	Description
/products	GET	Fetch product list
/materials	GET	Fetch material list
AI Recommendation
Endpoint	Method	Description
/rank	POST	Product-based material ranking
/recommend	POST	Predict cost, CO₂ & eco score
Dashboard & Analytics
Endpoint	Description
/dashboard/metrics	Global sustainability metrics
/dashboard/global-materials	Top eco materials
/dashboard/product-materials	Product-level analysis
/dashboard/material-trends	Material ranking trends
/dashboard/material-full-impact	Cost & CO₂ comparison
/dashboard/sustainability-kpis	KPI metrics
Report Export
Endpoint	Description
/dashboard/export/pdf	Download sustainability PDF
/dashboard/export/excel	Download Excel report
📊 Business Intelligence Dashboard

The system provides real-time analytics including:

Average Eco Score

Top Recommended Material

CO₂ Reduction Percentage

Cost Savings Percentage

Material sustainability ranking

Cost vs CO₂ comparison charts

Product-level bubble visualization

All charts are rendered dynamically using Chart.js.

📄 Sustainability Reports

EcoPackAI supports automated reporting:

PDF Report

Includes:

Selected product

Recommended materials

Suitability scores

Interpretation guide

Excel Report

Includes:

Material rankings

Suitability values

Structured analysis format

These reports are suitable for management and audit documentation.

🚀 Deployment

The project is deployed on Render with:

Flask backend

Static frontend serving

Pretrained ML models

CSV-based datasets

The application structure is deployment-ready and modular.

▶️ How to Run Locally
1️⃣ Clone Repository
git clone https://github.com/your-username/EcoPackAI.git
cd EcoPackAI

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Flask Server
python backend/app.py

5️⃣ Open Browser
http://localhost:5000

✅ Key Features

AI-driven material recommendations

Product-specific sustainability intelligence

Cost and CO₂ prediction

Interactive BI dashboard

PDF & Excel export

Secure APIs

Cloud deployment support

🔮 Future Scope

Integration with PostgreSQL database

Real-time Life Cycle Assessment (LCA)

Industry-specific recommendation models

Carbon compliance reporting

Multi-user authentication

Supply-chain optimization integration

🏁 Conclusion

EcoPackAI demonstrates how artificial intelligence can be applied to real-world sustainability challenges. By integrating machine learning, data analytics, and visualization into a unified platform, the system enables informed packaging decisions that balance environmental responsibility, product protection, and economic efficiency.

The project serves as a scalable foundation for next-generation sustainable supply chain intelligence systems.

👩‍💻 Author

Vrushali Nalawade
