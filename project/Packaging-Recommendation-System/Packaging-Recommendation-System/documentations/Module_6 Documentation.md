EcoPackAI – Module 6
Frontend UI (HTML + Bootstrap + JavaScript)

This module provides the frontend user interface for EcoPackAI, enabling users to interact with the Flask backend APIs to manage products, add material candidates, and view AI-driven material recommendations with ranking and metrics.

🎯 Purpose of This Module

Acts as the client-side interface for EcoPackAI

Connects to Module 5 Backend API (Flask)

Allows non-technical users to:

Create products

Add sustainable material candidates

Fetch AI material recommendations

View rankings and metrics visually

🚀 Features

Responsive UI using Bootstrap 5

Configurable backend connection (Base URL + API Key)

Product creation form

Material candidate input form

AI material recommendation trigger

JSON response viewer

Material ranking table

Client-side analytics metrics (RMSE, MAE)

No framework dependency (pure HTML + JS)

🛠 Tech Stack

HTML5

CSS3

Bootstrap 5.3

Vanilla JavaScript (ES6)

Fetch API

📂 File Structure
index.html
README.md


This module is intentionally lightweight and framework-free for easy deployment.

⚙️ Configuration
Backend Configuration Section

At the top of the UI, configure:

Base URL

http://127.0.0.1:5000


X-API-Key
Must match the API key defined in the Flask backend (API_KEY)

🔐 Authentication

All API calls include the header:

X-API-Key: <your-api-key>


Without a valid API key, requests will fail with 401 Unauthorized.

🧪 Functional Sections
1️⃣ Product Parameters

Create a new product

Optional constraints:

Max cost per kg

Max CO₂ per kg

Automatically triggers material recommendation after creation

2️⃣ Add Candidate Materials

Users can input:

Material name

Material type & subtype

Mechanical and sustainability attributes:

Strength

Weight capacity

Density

Biodegradability

Recyclability

Suitability score

Materials are stored in the backend database.

3️⃣ AI Material Recommendations

Fetches ranked materials from the backend AI model

Displays:

Raw JSON output

Ranking table

Computed metrics

4️⃣ Material Ranking Table

Displays:

Material name

Predicted cost (USD/kg)

Predicted CO₂ (kgCO₂/kg)

Final ranking score (lower is better)

5️⃣ Client-Side Metrics

Calculated in the browser:

RMSE (Cost)

MAE (Cost)

RMSE (CO₂)

MAE (CO₂)

Number of evaluated materials

Metrics are computed without backend dependency, purely for analysis/demo purposes.

▶️ How to Run
Step 1: Start Backend (Module 5 API)
python module5_api.py

Step 2: Open Frontend

Simply open index.html in your browser
OR

Serve via a local server:

python -m http.server 8080


Then open:

http://localhost:8080

🧩 Integration Notes

Backend must be running before using the UI

CORS is enabled in the Flask backend

Designed to integrate seamlessly with:

Module 5 Backend API

Module 7 BI Dashboard

📈 Limitations

No authentication UI (API key is manually entered)

No persistent frontend state (page refresh resets data)

Designed for demo / academic / prototype use
