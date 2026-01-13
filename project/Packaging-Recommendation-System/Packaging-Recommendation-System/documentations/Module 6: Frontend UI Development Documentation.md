# 🌱 EcoPackAI -- Module 6: Frontend Material Recommendation Interface

## 📌 Overview

Module 6 implements the **Frontend User Interface** for the EcoPackAI
system. This module allows users to interact with the AI-powered backend
to create products, add candidate materials, and receive **ranked
sustainable material recommendations** based on cost, CO₂ emissions, and
material properties.

The frontend acts as a bridge between users and the Flask REST API
developed in earlier modules.

------------------------------------------------------------------------

## 🎯 Key Features

-   🧾 Product creation with sustainability constraints
-   📦 Add and manage candidate packaging materials
-   🤖 AI-based material recommendation retrieval
-   📊 Ranked material comparison table
-   📈 Client-side performance metrics (RMSE, MAE)
-   🔐 Configurable API key authentication
-   🔗 Direct navigation to BI Dashboard (Module 7)

------------------------------------------------------------------------

## 🛠️ Technologies Used

### Frontend

-   HTML5
-   CSS3
-   Bootstrap 5.3
-   JavaScript (Vanilla)

### Backend (Integrated)

-   Flask REST API
-   JSON data exchange
-   API Key--based authentication

------------------------------------------------------------------------

## 🏗️ Module Architecture

    User Interface (HTML + JS)
            |
            | Fetch API (JSON)
            ↓
    Flask Backend (Modules 4 & 5)
            |
            ↓
    Database (Materials, Products, Predictions)

------------------------------------------------------------------------

## 🧩 Functional Components

### 1. Backend Configuration Panel

-   Base URL configuration
-   API key input for secure access

### 2. Product Parameters Form

-   Product name
-   Maximum cost per kg
-   Maximum CO₂ emissions per kg
-   Triggers AI recommendation generation

### 3. Candidate Materials Input

-   Material name, type, and subtype
-   Mechanical and sustainability attributes:
    -   Strength
    -   Density
    -   Weight capacity
    -   Biodegradability
    -   Recyclability
    -   Suitability score

### 4. AI Recommendations Output

-   Raw JSON response viewer
-   Ranked materials table with:
    -   Predicted cost
    -   Predicted CO₂ emissions
    -   Material rank score

### 5. Client-Side Metrics

-   RMSE (Root Mean Square Error)
-   MAE (Mean Absolute Error)
-   Metrics calculated against predicted values

------------------------------------------------------------------------

## 🔌 API Endpoints Used

### Create Product

    POST /api/products

### Add Materials

    POST /api/materials

### List Materials

    GET /api/materials

### Get Material Recommendations

    POST /api/recommendations/materials

------------------------------------------------------------------------

## ▶️ How to Run

1.  Start the Flask backend server
2.  Ensure API is running at `http://127.0.0.1:5000`
3.  Open the frontend HTML file in a browser
4.  Configure Base URL and API key
5.  Create a product and add materials
6.  View ranked AI recommendations and metrics

------------------------------------------------------------------------

## 📌 Output Screens

-   Product & material input forms
-   JSON-based AI recommendation response
-   Ranked comparison table
-   Client-side evaluation metrics

------------------------------------------------------------------------

## 🚀 Future Enhancements

-   UI validation and error handling
-   User authentication & role management
-   Advanced visualization integration
-   Responsive mobile optimization
-   Cloud deployment

------------------------------------------------------------------------

## 👨‍💻 Module Information

**Project:** EcoPackAI -- Sustainable Packaging Recommendation System\
**Module:** 6 -- Frontend Material Recommendation Interface
