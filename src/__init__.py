from flask import Blueprint

routes = Blueprint('forecast_controller', __name__)

from src.service import forecast_service
from src.persistence import forecast_dao
