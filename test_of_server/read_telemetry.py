import requests
from datetime import datetime

url = "http://localhost:3000/telemetry"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    for entry in data:
        print(entry)
else:
    print("Error:", response.status_code)
