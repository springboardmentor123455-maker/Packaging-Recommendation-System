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
  <img width="1919" height="644" alt="image" src="https://github.com/user-attachments/assets/6987d64d-3ebe-4c5d-b2ba-e34557d9f122" />

* Recommendation results
  <img width="1919" height="897" alt="image" src="https://github.com/user-attachments/assets/ab1313c1-4f32-4a4c-843a-075a87ad684c" />

  <img width="1919" height="720" alt="image" src="https://github.com/user-attachments/assets/de857163-1cba-498a-ab83-e89254151228" />


* BI Dashboard
 <img width="1918" height="958" alt="image" src="https://github.com/user-attachments/assets/34180167-9386-4faf-ab07-8354cc47f684" />

 <img width="1551" height="602" alt="image" src="https://github.com/user-attachments/assets/2f30009c-3c12-486d-b79f-4d2d5f9fb156" />

 <img width="1916" height="958" alt="image" src="https://github.com/user-attachments/assets/46b37c32-5274-4a70-9e65-cc31326c40fd" />

---
 Video Demo


https://github.com/user-attachments/assets/c7c20c23-8a54-4ef9-81c4-05ad066c2e1b


 
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
