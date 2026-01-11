## Milestone 3 – Backend & Frontend Integration (Lokesh Patil)

### Backend
- Developed Flask backend structured as a Python package.
- Implemented REST APIs:
  - `/api/health` for system status
  - `/api/recommend` for AI-based material recommendation
- Integrated PostgreSQL using SQLAlchemy.
- Implemented AI-based composite scoring for material ranking.

### AI Recommendation Logic
- Inputs: product weight, required strength.
- Ranking based on:
  - Mechanical strength
  - Cost efficiency
  - CO₂ emission impact
- Returned top 5 materials in JSON format.

### Frontend
- Built UI using HTML, CSS, and Bootstrap.
- Implemented input form for product parameters.
- Displayed ranked material recommendations dynamically.
- Connected frontend to backend via REST API.

### Testing
- Verified backend using CURL and browser.
- Validated frontend-backend integration with live data.
