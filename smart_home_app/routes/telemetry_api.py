from flask import Blueprint, request, jsonify
from data.models import TelemetryModel, ValidationError
from data.db import get_collection
from helpers.utils import doc_to_json
from helpers.helpers import get_telemetry_measurements, create_graph


telemetry_api = Blueprint('telemetry_api', __name__)

@telemetry_api.route('/api/telemetry', methods=['POST', 'GET'])
def telemetry():
    # maybe change if needed
    TELEMETRY_COLLECTION = get_collection('telemetry')
    if request.method == 'POST':
        if TELEMETRY_COLLECTION is None:
            return jsonify({"status": "error", "message": "Database not connected"}), 503

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
    elif request.method == 'GET':
        if TELEMETRY_COLLECTION is None:
            return jsonify({"status": "error", "message": "Database not connected"}), 503

        try:
            data = TELEMETRY_COLLECTION.find().sort("timestamp", -1)
            results = [doc_to_json(doc) for doc in data]
            return jsonify(results), 200

        except Exception as e:
            print(f"Error fetching telemetry: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500


@telemetry_api.get('/api/telemetry/latest')
def get_latest_telemetry():
    TELEMETRY_COLLECTION = get_collection('telemetry')
    if TELEMETRY_COLLECTION is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    try:
        latest_reading = TELEMETRY_COLLECTION.find_one(sort=[('timestamp', -1)])
        if not latest_reading:
            return jsonify({"status": "error", "message": "Latest telemetry data not found"}), 404

        return jsonify({"status": "ok", "data": latest_reading}), 200

    except Exception as e:
        return jsonify({"message": f"Error fetching latest reading: {e}"}), 500



# maybe we can delete it cause we don't really need this function
@telemetry_api.route('/api/telemetry/test', methods=['GET'])
def test_telemetry():
    TELEMETRY_COLLECTION = get_collection('telemetry')
    try:
        lines = 10
        df = get_telemetry_measurements(10, TELEMETRY_COLLECTION)
        return jsonify(
            {"status": "ok", "rows": len(df), "columns": df.columns.tolist(), "data": df.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500



@telemetry_api.route('/updateTelemetryTable')
def update_telemetry_table():
    lines = 10
    TELEMETRY_COLLECTION = get_collection('telemetry')
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