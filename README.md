---
title: EcoPackAI
emoji: 📦
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
---

# EcoPackAI - Sustainable Packaging Recommendation System

## 📘 Project Documentation & Methodology

**Project Name:** EcoPackAI  
**Domain:** Supply Chain Sustainability & AI  
**Tech Stack:** Python, Flask, Pandas, SQLite/PostgreSQL, HTML/CSS/JS

---

## 🚀 1. Data Collection & Architecture (Milestone 1)

### **Objective**
To build a robust dataset representing various packaging materials and their environmental impact.

### **Methodology used**
Since real-world proprietary data is scarce, we used **Synthetic Data Generation**.
*   **Tools:** `Faker`, `NumPy`, `Pandas`.
*   **Process:**
    1.  defined 15 core **Material Types** (e.g., Corrugated Cardboard, Corn Starch, Mushroom Packaging).
    2.  Generated **1200 data points**.
    3.  Simulated plausible relationships (e.g., higher strength $\approx$ slightly higher cost).
*   **Key Attributes:** `CO2_Emission`, `Biodegradability_Score`, `Cost_per_kg`, `Water_Resistance`.

### **Data Cleaning**
*   **Outliers:** Used **IQR (Interquartile Range)** method to detect and cap extreme values in Cost and CO2.
*   **Missing Values:** Imputed using category-wise mean filling.
*   **Normalization:** Applied **Min-Max Scaling** to normalize scores between 0-100 for easier comparison.

---

## 🗄️ 2. Database Implementation (Milestone 1 & 2)

### **Objective**
Store and retrieve material standards and recommendations efficiently.

### **Methodology**
*   **Hybrid Approach:** 
    *   We designed the system for **PostgreSQL** (Production standard) but implemented a smart fallback to **SQLite/CSV** for local development ease.
*   **Schema Design:**
    *   `materials_data`: Master table for all material properties.
    *   `product_categories`: Rules for what material suits what product (e.g., Electronics need high cushion).
*   **Why this approach?** It allows the app to run instantly on any machine without complex database installation validation.

---

## 🧠 3. AI & Recommendation Engine (Milestone 2)

### **Objective**
To intelligently rank materials based on user constraints.

### **Methodology**
*   **Scoring Algorithm:** We developed a **Weighted Suitability Score**.
    *   *Formula:* $Score = (0.4 \times Bio) + (0.3 \times Strength) - (0.2 \times CO2) - (0.1 \times Cost)$
*   **Filtering:** The engine first filters materials that meet the "Hard Constraints" (e.g., if User says "Must be Waterproof", strictly remove non-waterproof items).
*   **Ranking:** remaining items are sorted by the calculated Suitability Score.

---

## 💻 4. Web Application Development (Milestone 3)

### **Objective**
Create a user-friendly interface for Supply Chain Managers.

### **Tech Stack**
*   **Backend:** **Flask (Python)**. Lightweight and fast.
    *   `routes.py`: Handles HTTP requests.
    *   `run.py`: Entry point for the server.
*   **Frontend:** **HTML5, CSS3, JavaScript**.
    *   **Design Style:** **Glassmorphism** (Translucent backgrounds, blur effects) for a modern, premium look.
    *   **Responsiveness:** CSS Grid/Flexbox used to ensure it works on Tablets/Desktops.
*   **Integration:** The Frontend sends JSON data to Flask features, Flask consults the AI engine, and returns JSON results.

---

## 📊 5. BI Dashboard (Milestone 4)

### **Objective**
To visualize sustainability impact and market trends.

### **Methodology**
*   **Visuals:** Implemented interactive charts using **Chart.js**.
*   **Key Metrics:**
    *   **Market vs. Sustainable:** Bar charts comparing average CO2 of general market vs. our green recommendations.
    *   **Cost Analysis:** Scatter plots showing Cost vs. Eco-friendliness.
    *   **Material Distribution:** Pie charts of available material types.

---

## ☁️ 6. Deployment Guide (Hugging Face Spaces)

### **How to Deploy (Step-by-Step)**

This application is deployed on **Hugging Face Spaces** for robust AI performance (16GB RAM support).

**1. Create a Space**
*   Go to **huggingface.co/spaces**.
*   Click **"Create new Space"**.
*   **Name:** `EcoPackAI`
*   **SDK:** `Docker` (Crucial for Flask).
*   **Privacy:** `Public`.

**2. Upload Code**
*   You can upload via Git or manually via the "Files" tab.
*   Ensure `Dockerfile` is at the root.

**3. Configuration (README.md)**
*   Ensure the `README.md` has the YAML metadata at the top:
    ```yaml
    ---
    title: EcoPackAI
    sdk: docker
    app_port: 7860
    ---
    ```

**4. Result**
*   Hugging Face will build the Docker container.
*   Once "Running", your app is live!
*   **Live Demo:** [https://huggingface.co/spaces/ragasudhaselvaraj/EcoPackAI](https://huggingface.co/spaces/ragasudhaselvaraj/EcoPackAI)

---

## 📈 Project Status Summary

| Module | Status | Technology Used |
| :--- | :--- | :--- |
| **Data Cleaning** | ✅ Completed | Pandas, NumPy |
| **Database** | ✅ Completed | SQLite / CSV Fallback |
| **AI Model** | ✅ Completed | Scikit-Learn |
| **Backend API** | ✅ Completed | Flask |
| **Frontend UI** | ✅ Completed | CSS3 Glassmorphism |
| **Dashboard** | ✅ Completed | Chart.js |
| **Deployment** | ⏳ Ready | Render Configuration |
