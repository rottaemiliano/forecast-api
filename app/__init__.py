from flask import Blueprint

routes = Blueprint('forecast_controller', __name__)

from app.service import forecast_service
from app.persistence import forecast_dao
