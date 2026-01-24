📦EcoPackAI - AI-Powered Sustainable Packaging Recommendation System
Milestone 1 – Data Collection & Preprocessing
This project is part of the Infosys Springboard Virtual Internship (AI Domain). The goal is to build an intelligent system that recommends eco-friendly packaging materials based on sustainability metrics.

✅ Milestone 1 Completed Tasks
1️⃣ Data Import & Storage
Imported a 500-row synthetic eco-material dataset

Stored it inside a MySQL database (materials table)

Connected MySQL to Jupyter Notebook using mysql.connector

Loaded dataset into Pandas DataFrame

2️⃣ Data Quality Checks
Performed essential checks:

Dataset shape

Missing values

Duplicate rows

Descriptive statistics (df.describe())

3️⃣ Outlier Detection (IQR Method)
Identified outliers in:

Weight

Cost

CO₂ Emissions

Used IQR to calculate:

Q1, Q3

Lower bound

Upper bound

Outlier count per column

4️⃣ Outlier Treatment (Clipping)
df_clean[numeric_cols] = df[numeric_cols].clip(lower_bound, upper_bound, axis=1)

✔ All outliers were successfully removed.

5️⃣ Cleaned Dataset Export
Exported cleaned dataset as:

materials_cleaned.csv

This file will be used in further milestones.

✅ Milestone 2 (Week 3–4)
🔹 Module 3: Machine Learning Dataset Preparation

In this phase, we prepare the dataset for training ML models by performing structured preprocessing and feature selection.

Key tasks completed:

Split the dataset into training and testing sets for unbiased evaluation

Selected important features for prediction such as:
material safety, strength, shipping category, recyclability, biodegradability, cost factors, and CO₂ factors

Generated target variables to support predictions:

📌 Cost Prediction

🌍 CO₂ Impact Prediction

Created a clean ML pipeline including:

Feature engineering

Data scaling / normalization

Final dataset preparation for model training

🔹 Module 4: AI Recommendation Model (ML-Based)

This module focuses on training machine learning models and creating an intelligent packaging recommendation engine based on predicted performance.

Model Training Implemented:

✅ Random Forest Regressor → for Cost Prediction

✅ XGBoost Regressor → for CO₂ Footprint Prediction

Model Evaluation Metrics Used:

📉 RMSE (Root Mean Squared Error)

📌 MAE (Mean Absolute Error)

📊 R² Score

Final Output of this Module:

Built an AI-powered material ranking system that recommends the most suitable packaging material based on:
✅ predicted cost, ✅ environmental impact (CO₂), ✅ material strength, and ✅ safety suitability.

✅ Milestone 3 (Week 5–6)
🔹 Module 5: Flask Backend API Development

In this milestone, we built a complete Flask-based REST API to power the Packaging Recommendation System.

Key backend deliverables:

Developed REST APIs for:

📦 Product input handling

🤖 AI-based packaging material recommendations

🌱 Environmental / sustainability score computation

Connected backend services with a PostgreSQL / Database layer for storage & retrieval

Implemented structured and consistent JSON response formats across endpoints

Secured APIs with clean request validation and reliable endpoint handling

🔹 Module 6: Frontend UI Development

To make the system interactive and user-friendly, we designed a responsive frontend interface for smooth user experience.

Frontend features implemented:

Built UI using:

✅ HTML

✅ CSS

✅ Bootstrap

Created dynamic input forms to collect product parameters such as:
category, weight, fragility, shipping distance

Displayed AI-generated material recommendations in a clean format

Presented results using:
📊 Ranking table
📌 Comparison metrics (Cost, CO₂, Strength, Final Score)

📁 Project Structure
Packaging-Recommendation-System/ │ README.md │ requirements.txt │ ├── notebooks/ │ _Data_preprocessing │ ├── data/ │ materials_cleaned.csv | | Flask Backend API | | Frontend UI Development |

🛠️ Tools & Technologies Used

Python - Flask 

HTML

CSS 

Bootstrap

Pandas

NumPy

Jupyter Notebook

VS Code

MySQL

Git & GitHub

🚀 Upcoming Milestone: Feature Engineering
Milestone 2 will include:

Sustainability Score

CO₂ Impact Index

Cost Efficiency Index

Durability Normalization

Correlation Heatmaps & EDA Visualizations

📞 Contact
Maintainer: Ayush Kumar Pandey Email: ayushpandey1974@gmail.com

GitHub: github.com/ayushpandey3357
