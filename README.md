🌱 EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

EcoPackAI is an AI-driven web application that recommends sustainable and cost-efficient packaging materials based on product requirements. The system combines machine learning models, sustainability metrics, business intelligence dashboards, and cloud deployment to support data-driven and environmentally responsible packaging decisions.

📌 Problem Statement

Selecting eco-friendly packaging materials is challenging because it requires balancing multiple factors:

• Environmental impact (CO₂ emissions, biodegradability)
• Material performance (strength, weight capacity, water resistance)
• Cost efficiency

Traditional selection approaches are manual, subjective, and lack quantitative evaluation. EcoPackAI addresses this challenge by providing an automated, AI-based recommendation system.

🎯 Project Objectives

• Collect and manage eco-friendly packaging material data
• Perform data cleaning and feature engineering
• Build machine learning models for cost and CO₂ impact prediction
• Recommend optimal packaging materials using AI
• Develop an interactive web-based user interface
• Build a BI dashboard for sustainability insights
• Deploy the application on cloud infrastructure
• Provide complete technical documentation and demo

🧠 System Overview

EcoPackAI consists of the following layers:

• Data Layer → PostgreSQL database storing material and product data
• AI Layer → Machine learning models (Random Forest, XGBoost)
• Backend Layer → Flask REST APIs with business logic
• Frontend Layer → HTML, CSS, Bootstrap, JavaScript
• BI Layer → Dashboards, KPIs, sustainability reports
• Deployment Layer → Render cloud platform

🛠 Technology Stack

• Programming Language → Python
• Backend Framework → Flask
• Machine Learning → Random Forest, XGBoost
• Database → PostgreSQL
• Frontend → HTML, CSS, Bootstrap, JavaScript
• Data Processing → Pandas, NumPy
• Visualization → Chart.js, Matplotlib
• Deployment → Render

⚙ Key Features

• AI-based packaging material recommendation
• Cost efficiency prediction
• CO₂ impact estimation
• Sustainability scoring
• Material ranking system
• Business Intelligence dashboard
• Exportable sustainability reports
• Cloud deployment with PostgreSQL integration

📊 Machine Learning Models

• Random Forest Regressor
→ Used for predicting packaging cost efficiency
→ Handles non-linear relationships effectively

• XGBoost Regressor
→ Used for predicting CO₂ environmental impact
→ Provides high accuracy for complex feature patterns

• Model evaluation metrics used:
→ RMSE
→ MAE
→ R² Score

🔗 API Endpoints

► /recommend
• HTTP Method → POST
• Purpose → Returns top recommended packaging materials
• Inputs → Product weight, product fragility
• Output → Ranked materials with predicted cost and CO₂ impact

► /environment-score
• HTTP Method → POST
• Purpose → Evaluates environmental sustainability
• Output → CO₂ impact index and material suitability score

📊 Business Intelligence (BI) Dashboard & Sustainability Reporting

The BI dashboard transforms AI-generated recommendations into actionable insights for sustainability and cost optimization.

🎯 Dashboard Objectives
• Visualize AI recommendations
• Compare baseline vs recommended materials
• Measure CO₂ emission reduction
• Measure cost savings
• Provide exportable sustainability reports

📈 Key Dashboard Metrics
• CO₂ Reduction Percentage
• Cost Reduction Percentage
• Material Performance Score
• Sustainability Score (0–100)

📋 Dashboard Functional Modules
• Baseline vs Recommended Material Comparison
• Material Comparison Table
• KPI Cards (Average Cost Reduction, Average CO₂ Reduction)
• Material Suitability Distribution
• Top Performing Materials

📊 Visualization Types
• Pie charts
• KPI cards
• Comparison tables

📤 Sustainability Report Export
• Material Comparison Report (Excel)
• Material Performance Report (Excel)
• Sustainability Summary Report (Excel)

🚀 Deployment Details

• Cloud Platform → Render
• Application Type → Web Service
• Database → PostgreSQL Cloud Database

🔗 Live Application Link:
https://my-packaging-recommendation-system.onrender.com/

▶ How to Run the Project Locally

• Clone the project repository
• Create a virtual environment
• Install required dependencies
• Configure PostgreSQL environment variables
• Run the Flask application(local_app.py)
• Don't run app.py because it is a deployed code it won't works in the local

📄 Documentation and Demo

• Project Report → Included in the repository
link →  https://drive.google.com/drive/folders/1NYe67iTyC0tsSrTnaa05xgEIkZyBdGxo?usp=drive_link

• Video Demo Link →
https://drive.google.com/file/d/18Ijd5YpUXgIBRVOi_AXpxgBhLOady-lM/view

• PPT Presentation Link →
https://drive.google.com/drive/folders/1BC3py8AlXgBCHcCSl754JSDp1QGtOFVC

📌 Results and Outcomes

• Accurate AI-based packaging recommendations
• Effective balance between sustainability and cost
• Fully deployed cloud-based application
• Modular, scalable, and industry-aligned system

🔮 Future Enhancements

• Integration of real-time market pricing
• Advanced deep learning models
• User authentication and role-based access
• Real-time dashboards and analytics
• Enterprise-scale deployment with CI/CD

👩‍🎓 Author

• Name → Nandhitha PT
• Role → College Student | AI & Data Science Enthusiast
