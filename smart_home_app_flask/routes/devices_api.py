from flask import jsonify, Blueprint, request, current_app
import requests

devices_api = Blueprint('devices_api', __name__)




# Method to fetch current values from esp32 to build a webpage
# need to test it with esp32
@devices_api.route('/api/status', methods=['GET'])
def status():
    ESP32_IP = current_app.config['ESP32_IP']
    # we would need to modify the code to take only a value from request not a json
    # light_range = requests.get(f"{ESP32_IP}/light")
    # curtain = requests.get(f"{ESP32_IP}/curtain")
    # climate = requests.get(f"{ESP32_IP}/climate")
    # testing type of answers from esp32
    light_range = 40 # in percent
    curtain_range = 60 # in percent
    climate = 'warm' # we have 3 modes: warm, cool, off
    return jsonify({"status": "ok", "light": light_range, "curtain": curtain_range, "climate": climate})

@devices_api.route('/api/light/power', methods=['POST'])
def light_power():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    state = data['state']

    if state == "on":
        r = requests.get(f"{ESP32_IP}/light/on")
    else:
        r = requests.get(f"{ESP32_IP}/light/off")

    return jsonify({"status": "ok", "esp32_response": r.text})

@devices_api.route('/api/light/intensity', methods=['POST'])
def light_intensity():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    value = data['value']
    r = requests.get(f"{ESP32_IP}/light/intensity?value={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})


@devices_api.post('/api/curtain')
def curtain_position():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    value = data['value']
    r = requests.get(f"{ESP32_IP}/curtain?value={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})



# Climate mode
@devices_api.post("/api/climate")
def climate_mode():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    mode = data["mode"]
    r = requests.get(f"{ESP32_IP}/climate?mode={mode}")
    return jsonify({"status": "ok", "esp32_response": r.text})

# Default temperature
@devices_api.post("/api/target_temperature")
def target_temperature():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    value = data['value']
    r = requests.get(f"{ESP32_IP}/target_temperature?value={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})


@devices_api.post("/api/curtain_time")
def set_curtain_time():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    value = data['time']
    r = requests.get(f"{ESP32_IP}/curtain?time={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})


@devices_api.post("/api/security")
def security():
    ESP32_IP = current_app.config['ESP32_IP']
    data = request.get_json()
    value = data['status']
    r = requests.get(f"{ESP32_IP}/security?status={value}")
    return jsonify({"status": "ok", "esp32_response": r.text})