from pymongo import MongoClient
from datetime import datetime


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")

    db = client.Smart_Home

    telemetry_collection = db.telemetries
    telemetry_data = {
        "timestamp": datetime.now(),
        "temperature": 25.5,
        "humidity": 60,
        "light": 300,
        "motion": True,
    }

    result = telemetry_collection.insert_one(telemetry_data)
    print(f"Inserted document ID: {result.inserted_id}")

    client.close()
