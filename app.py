from flask import Flask
from app.controller.forecast_controller import forecast_controller

app = Flask(__name__)

app.register_blueprint(forecast_controller)

if __name__ == "__main__":
    app.config["DEBUG"] = False
    app.run(host='localhost', port=5000)
