# 🌱 EcoPackAI -- Module 7: Business Intelligence Dashboard

## 📌 Overview

Module 7 of **EcoPackAI** implements a **Business Intelligence (BI)
Dashboard** that provides actionable insights into the environmental and
economic impact of eco-friendly packaging solutions. The dashboard
visualizes key sustainability metrics such as **CO₂ reduction**, **cost
savings**, and **material usage trends**, helping stakeholders make
informed decisions.

## 🎯 Features

-   📊 Interactive data visualization using **Plotly.js**
-   🌍 CO₂ emission reduction analysis
-   💰 Cost savings comparison with baseline materials
-   📦 Material usage trend visualization
-   📄 Export sustainability reports as **PDF**
-   📈 Export BI metrics as **Excel**
-   🔗 Seamless integration with Flask backend API

## 🛠️ Technologies Used

### Frontend

-   HTML5
-   CSS3
-   Bootstrap 5.3
-   JavaScript

### Visualization & Reporting

-   Plotly.js
-   jsPDF
-   SheetJS (XLSX)

### Backend (Integrated)

-   Flask REST API
-   JSON-based data exchange

## 🏗️ Module Architecture

Frontend (HTML + JS) → Flask Backend → Database

## 📊 Dashboard Metrics

-   **CO₂ Reduction (%)**
-   **Cost Savings (%)**
-   **Total Materials Analyzed**

## 📈 Visualizations

-   Bar Chart: CO₂ Reduction per material
-   Bar Chart: Cost Savings per material
-   Pie Chart: Material usage distribution

## 📤 Export Options

### PDF Report

-   Sustainability summary per material
-   CO₂ reduction and cost savings

### Excel Report

-   Tabular BI metrics
-   Material-wise sustainability data

## 🔌 API Endpoint

GET http://127.0.0.1:5000/api/module7/bi-data

## ▶️ How to Run

1.  Start the Flask backend server
2.  Open dashboard.html in a browser
3.  Ensure backend API runs on port 5000

## 📌 Future Enhancements

-   Authentication
-   Real-time analytics
-   Advanced filtering
-   Cloud deployment

## 👨‍💻 Project

EcoPackAI -- Sustainable Packaging Recommendation System Module 7:
Business Intelligence Dashboard
