import requests

response = requests.post(
    "http://127.0.0.1:5000/recommend",
    json={
        "weight": "Medium",
        "fragility": "High"
    }
)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
