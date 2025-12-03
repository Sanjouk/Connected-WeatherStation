from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import requests
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

import json
import os

from data.db import init_db, get_collection
from helpers.helpers import create_graph, get_telemetry_measurements

# Flask init
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Smart_Home"

# Database init
db = init_db(app)

TELEMETRY_COLLECTION = get_collection("telemetry")
SETTINGS_COLLECTION = get_collection("settings")

# prospect user collection
# USERS_COLLECTION = get_collection("users")
# DEVICES_COLLECTION = get_collection("devices")
# LOGS_COLLECTION = get_collection("logs")


GRAPH_DIR = 'graphs'

@app.route(f'/{GRAPH_DIR}/<path:filename>')
def serve_graphs(filename):
    """Serves files from the custom 'graphs' directory."""
    return send_from_directory(GRAPH_DIR, filename)

# ESP32 init

ESP32_IP = "https://192.168.1.50"

if TELEMETRY_COLLECTION is None:
    print("WARNING: Database connection failed during startup. API endpoints will not work.")

if SETTINGS_COLLECTION is None:
    print("WARNING: Database connection failed during startup. API endpoints will not work.")


# Pydantic type for our db model

class TelemetryModel(BaseModel):
    temperature: float
    humidity: float
    light: float
    motion: float
    timestamp: datetime = Field(default_factory=datetime.now)

# Part of page view
@app.route('/')
def index():
    return (render_template('index.html'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/governance')
def governance():
    return render_template('governance.html')

@app.route('/telemetryTable')
def telemetry_table():
    lines = 10
    df = get_telemetry_measurements(lines=lines, collection=TELEMETRY_COLLECTION)
    measurement_columns = [
        ('temperature', 'Hourly Temperature (°C)'),
        ('humidity', 'Hourly Relative Humidity (%)'),
        ('light', 'Hourly Ambient Light (lux)'),
    ]

    graphs = []
    for col_name, title in measurement_columns:

        graph_json = create_graph(
            df,
            x_col='timestamp',
            y_col=col_name,
            title=title
        )

        # Store the JSON string along with the graph's title and ID for the template
        graphs.append({
            'id': col_name.replace('_', '-'),  # unique ID for the HTML div
            'title': title,
            'json': json.loads(graph_json)
        })

    # 4. Render the template, passing the list of graph data
    return render_template('telemetry_table.html', graphs=graphs)



@app.route('/updateTelemetryTable')
def update_telemetry_table():
    lines = 10
    df = get_telemetry_measurements(lines=lines, collection=TELEMETRY_COLLECTION)
    measurement_columns = [
        ('temperature', 'Hourly Temperature (°C)'),
        ('humidity', 'Hourly Relative Humidity (%)'),
        ('light', 'Hourly Ambient Light (lux)'),
    ]

    graphs_map = {}
    for col_name, title in measurement_columns:

        graph_json = create_graph(
            df,
            x_col='timestamp',
            y_col=col_name,
            title=title
        )

        graph_id = col_name.replace('_', '-')

        # Populate the map with the graph ID as the key, and the JSON data as the value
        graphs_map[graph_id] = graph_json

        # Return the dictionary instead of the list
        # jsonify will convert the dict into the JSON object the client expects
    return jsonify(graphs_map)

# @app.route('/telemetryTable')
# def telemetry_table():
#     # 1. Ensure the graphs directory exists
#     if not os.path.exists(GRAPH_DIR):
#         os.makedirs(GRAPH_DIR)
#         print(f"Created graph directory: {GRAPH_DIR}")
#
#     lines = 10
#     df = get_telemetry_measurements(lines=lines, collection=TELEMETRY_COLLECTION)
#     measurement_columns = [
#         ('temperature', 'Hourly Temperature (°C)'),
#         ('humidity', 'Hourly Relative Humidity (%)'),
#         ('light', 'Hourly Ambient Light (lux)'),
#     ]
#
#     graphs = []
#     print(df)
#     for col_name, title in measurement_columns:
#
#         # Call the updated create_graph, which saves the HTML file and returns the path
#         graph_filepath = create_graph(
#             df,
#             x_col='timestamp',
#             y_col=col_name,
#             title=title,
#             output_dir=GRAPH_DIR # Pass the output directory
#         )
#
#         # Store the filepath for the template instead of the JSON string
#         graphs.append({
#             'id': col_name.replace('_', '-'),  # unique ID for the HTML iframe
#             'title': title,
#             'filepath': graph_filepath # Changed 'json' to 'filepath'
#         })
#
#     # 4. Render the template, passing the list of graph data
#     return render_template('telemetry_table.html', graphs=graphs)


# @app.route('/api/telemetry/test')
# def test_telemetry():
#     return null



# PART OF API
def doc_to_json(document):
    if document:
        document['_id'] = str(document['_id'])
        if 'timestamp' in document and isinstance(document['timestamp'], datetime):
            document['timestamp'] = document['timestamp'].isoformat()
        return document
    return None
@app.route('/api/telemetry', methods=['POST'])
def post_telemetry():
    if TELEMETRY_COLLECTION is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    # try:
        data = request.get_json()

        # required_fields = ['temperature', 'humidity']
        # for field in required_fields:
        #     if field not in data:
        #         return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
        #
        # document = {
        #     "timestamp": datetime.now(),  # Replaces Mongoose's default: Date.now
        #     "temperature": data.get('temperature'),
        #     "humidity": data.get('humidity'),
        #     "light": data.get('ldr', data.get('light')),  # Use 'ldr' if present, otherwise 'light'
        #     "motion": data.get('pir', data.get('motion'))  # Use 'pir' if present, otherwise 'motion'
        # }
        #
        # try:
        #     document['light'] = float(document['light'])
        #     document['motion'] = float(document['motion'])
        # except (ValueError, TypeError) as e:
        #     return jsonify({"status": "error", "message": f"Data type error for light/motion: {e}"}), 400
        #
        # result = TELEMETRY_COLLECTION.insert_one(document)
        # print(f"Saved telemetry with ID: {result.inserted_id}")
        # return jsonify({"status": "ok"}), 200
    try:
        data = request.get_json()
        try:
            telemetry = TelemetryModel(**data)
        except ValidationError as e:
            return jsonify({"status": "error", "message": e.errors()}), 400

        result = TELEMETRY_COLLECTION.insert_one(telemetry.dict())
        print(f"Saved telemetry with ID: {result.inserted_id}")
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error saving telemetry: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/telemetry/latest', methods=['GET'])
def get_latest_telemetry():
    if TELEMETRY_COLLECTION is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    try:
        latest_reading = TELEMETRY_COLLECTION.find_one(sort=[("timestamp", -1)])

        if not latest_reading:
          return jsonify({"message": "No readings found."}), 404

        return jsonify(doc_to_json(latest_reading)), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching latest reading: {e}"}), 500


@app.route('/api/telemetry', methods=['GET'])
def get_all_telemetry():
    if TELEMETRY_COLLECTION is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    try:
        data = TELEMETRY_COLLECTION.find().sort("timestamp", -1)
        results = [doc_to_json(doc) for doc in data]
        return jsonify(results), 200

    except Exception as e:
        print(f"Error fetching telemetry: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/api/telemetry/test', methods=['GET'])
def test_telemetry():
    try:
        lines = 10
        df = get_telemetry_measurements(10, TELEMETRY_COLLECTION)
        return jsonify(
            {"status": "ok", "rows": len(df), "columns": df.columns.tolist(), "data": df.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# API for ESP32 to post data
# Light power
@app.route("/api/light/power")
def light_power():
    data = request.get_json()
    state = data['state']

    if state == "on":
        r = requests.get(f"{ESP32_IP}/light/on")
    else:
        r = requests.get(f"{ESP32_IP}/light/off")

    return jsonify({"status": "ok", "esp32_response": r.text})

# Light intensity
@app.route("/api/light/intensity")
def light_intensity():
    data = request.get_json()
    value = data['value']
    r = requests.get(f"{ESP32_IP}/light/intensity?value={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})



# Curtain position
@app.post("/api/curtain")
def curtain_position():
    data = request.get_json()
    value = data['value']
    r = requests.get(f"{ESP32_IP}/curtain?value={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})

# Climate mode
@app.post("/api/climate")
def climate_mode():
    data = request.get_json()
    mode = data["mode"]
    r = requests.get(f"{ESP32_IP}/climate?mode={mode}")
    return jsonify({"status": "ok", "esp32_response": r.text})

# Default temperature
@app.post("/api/target_temperature")
def target_temperature():
    data = request.get_json()
    value = data['value']
    r = requests.get(f"{ESP32_IP}/target_temperature?value={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})


if __name__ == '__main__':
    # Flask default port is 5000. Using PORT 3000 to match your old setup.
    PORT = 3000
    print("-" * 50)
    print(f"Flask Server running at http://127.0.0.1:{PORT}")
    print(f"Frontend served from: http://127.0.0.1:{PORT}/")
    print(f"API access point: http://127.0.0.1:{PORT}/api/telemetry/latest")
    print("-" * 50)
    # The debug=True flag enables auto-reloading during development
    app.run(host="0.0.0.0", debug=True, port=PORT)