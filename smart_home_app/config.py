class Config:
    # Flask settings
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 3000

    # MongoDB settings
    MONGO_URI = "mongodb://localhost:27017/Smart_Home"

    # Graph directory
    GRAPH_DIR = "graphs"

    # ESP32 IP
    ESP32_IP = "https://192.168.1.50"

    # Database collections
    TELEMETRY_COLLECTION = "telemetry"
    SETTINGS_COLLECTION = "settings"
    USERS_COLLECTION = "users"
    DEVICES_COLLECTION = "devices"
    LOGS_COLLECTION = "logs"
