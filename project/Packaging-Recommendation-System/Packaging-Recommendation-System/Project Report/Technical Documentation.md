# 🌱 EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

EcoPackAI is an AI-driven web application that recommends **sustainable and cost-efficient packaging materials** based on product requirements. The system leverages machine learning, cloud databases, and business intelligence dashboards to support **environmentally responsible and data-driven packaging decisions**.

---

## 1️⃣ Problem Statement

Choosing eco-friendly packaging materials is challenging due to the need to balance:

* Environmental impact (CO₂ emissions, biodegradability)
* Cost efficiency
* Material performance and durability

Traditional selection methods are manual, subjective, and inefficient. Poor packaging choices can increase costs and environmental damage. **EcoPackAI solves this problem by providing an AI-based recommendation system** that objectively evaluates packaging materials using data-driven intelligence.

---

## 2️⃣ Objectives

* Recommend eco-friendly packaging materials using AI
* Reduce environmental impact and CO₂ emissions
* Optimize packaging cost and material usage
* Provide actionable insights through dashboards and APIs

---

## 3️⃣ Tech Stack

**Frontend**

* HTML
* CSS
* Bootstrap

**Backend**

* Python
* Flask

**Database**

* PostgreSQL (Cloud)

**Machine Learning**

* Random Forest
* XGBoost

**Deployment**

* Render / Heroku

**Tools**

* GitHub
* VS Code

---

## 4️⃣ System Architecture

**Flow:**

User → Web UI → Flask REST API → ML Models → PostgreSQL Database → Recommendation Response

The system follows a modular architecture where data storage, AI prediction, backend logic, and frontend presentation are decoupled for scalability and maintainability.

*(Optional: Add system architecture diagram here)*

---

## 5️⃣ Features

* User input for packaging requirements (weight, fragility)
* AI-based packaging recommendation engine
* Sustainability scoring and ranking
* Business Intelligence (BI) dashboard visualization
* Cloud-hosted PostgreSQL database
* REST API integration

---

## 6️⃣ Database Design

**Database Name:** ecopackai_db

**Tables Used:**

* **materials**

  * id
  * name
  * eco_score
  * cost
  * co2_emission

* **recommendations**

  * id
  * user_input
  * recommended_material
  * sustainability_score

---

## 7️⃣ API Endpoints

| Method | Endpoint   | Description              |
| ------ | ---------- | ------------------------ |
| GET    | /          | Home page                |
| POST   | /predict   | Packaging recommendation |
| GET    | /dashboard | BI Dashboard             |

---

## 8️⃣ Deployment Details

* **Platform:** Render / Heroku
* **Database:** PostgreSQL Cloud Instance

**Environment Variables:**

* DATABASE_URL
* SECRET_KEY

🔗 **Live URL:**
https://my-packaging-recommendation-system.onrender.com

---

## 9️⃣ How to Run Locally

```bash
git clone <repo-url>
cd project-folder
pip install -r requirements.txt
python app.py
```

⚠️ *Note: For this project, use `local_app.py` for local execution if cloud configuration is present in `app.py`.*

---

## 🔟 Screenshots

(Add the following screenshots here)

* Web UI
* Recommendation results
* BI Dashboard
* PostgreSQL database connection

---

## 🔮 Future Enhancements

* Machine learning model optimization
* User authentication and role-based access
* Advanced analytics and real-time dashboards
* Integration of real-time market pricing
* CI/CD pipeline and enterprise-scale deployment

---

## 👨‍🎓 Author

**Abrar H**
Integrated MCA Student
Amrita Vishwa Vidyapeetham, Kochi Campus
