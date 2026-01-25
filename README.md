# Packaging Recommendation System

An AI-based Packaging Recommendation System that suggests the best packaging materials for a product based on **Cost, CO₂ emissions, Strength, and Sustainability**.  
It also provides a **Dashboard** to visualize material trends and savings.

---

## 🌐 Live Deployment (Render)

✅ Main Application (UI):  
https://packaging-recommendation-system-5.onrender.com/

✅ Dashboard (UI):  
https://packaging-recommendation-system-5.onrender.com/dashboard

---

## ✅ Key Features

- Add packaging materials (recyclable / biodegradable / strength / cost / CO₂)
- Generate packaging recommendations for products
- Save product + top recommendations in database
- Dashboard insights:
  - Total products
  - Total recommendations
  - Top materials used
  - Estimated cost savings
  - Estimated CO₂ reduction
- Export sustainability report as Excel

---

## 🛠 Tech Stack

**Backend**
- Python (Flask)
- Flask-SQLAlchemy (ORM)
- PostgreSQL (Render cloud database)
- Gunicorn (Production server)
- Flask-CORS

**Frontend**
- HTML, CSS, JavaScript
- Charts + dashboard visualization

**Deployment**
- Render (Web Service + PostgreSQL)

---

## 📌 Project Structure

Packaging-Recommendation-System/
│
├── Backend/
│ ├── templates/
│ │ ├── index.html
│ │ ├── dashboard.html
│ │
│ ├── app.py
│ ├── config.py
│ ├── db.py
│ ├── models.py
│ ├── requirements.txt
│ ├── Procfile
│ └── runtime.txt
│
└── README.md

yaml
Copy code

---

## 🚀 API Endpoints

### ✅ Health Check
- `GET /`
Returns JSON status message.

### ✅ Initialize Database (run once after deploy)
- `GET /init-db`

### ✅ Materials
- `POST /api/material` → Add a new material  
- `GET /api/materials` → Fetch all materials

### ✅ Products
https://packaging-recommendation-system-5.onrender.com/api/product → Add product
https://packaging-recommendation-system-5.onrender.com/api/product-recommend → Save product + generate recommendations

### ✅ Recommendation Engine
- `POST /api/recommend` → Get top 5 recommendations (without saving)

### ✅ Dashboard APIs
https://packaging-recommendation-system-5.onrender.com/api/dashboard/summary

https://packaging-recommendation-system-5.onrender.com/api/dashboard/material-trends

https://packaging-recommendation-system-5.onrender.com/api/dashboard/savings


### ✅ Export Excel
https://packaging-recommendation-system-5.onrender.com/api/dashboard/export/excel


---

## ✅ How Recommendation Score is Calculated

Final Score is calculated using:

- Strength
- CO₂ impact
- Cost
- Recyclable bonus
- Fragile bonus
- Category bonus (Food/Electronics/Furniture etc.)

---

## 🔧 Local Setup (Optional)

1) Clone the repo
```bash
git clone <https://github.com/ayushpandey3357>
cd Packaging-Recommendation-System/Backend
