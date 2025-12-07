from flask import Flask, jsonify
from config import Config

from data.db import init_db
from routes.settings_api import settings_api
from routes.views import views
from routes.telemetry_api import telemetry_api
from routes.devices_api import devices_api




app = Flask(__name__)
app.config.from_object(Config)

db = init_db(app)


app.register_blueprint(views)
app.register_blueprint(telemetry_api)
app.register_blueprint(devices_api)
app.register_blueprint(settings_api)




if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host=app.config["HOST"], port=app.config["PORT"])