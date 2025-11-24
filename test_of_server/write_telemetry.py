import requests
from datetime import datetime

url = "http://localhost:3000/telemetry"


telemetry_data = {
    "timestamp": datetime.now().isoformat(),
    "temperature": 24.5,
    "humidity": 55,
    "light": 320,
    "motion": True,
}

response = requests.post(url, json=telemetry_data)
print(response.status_code)
print(response.json())
