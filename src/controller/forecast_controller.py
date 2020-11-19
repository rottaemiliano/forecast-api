import json

from flask import Blueprint
from flask import request, json
from src import forecast_dao, forecast_service

forecast_controller = Blueprint('account_api', __name__)
fs = forecast_service.ForecastService
fd = forecast_dao.ForecastDAO

@forecast_controller.route('/cidade', methods=['POST'])
def cidade():
    if 'id' in request.args:
        city_id = int(request.args['id'])

        forecast_json = fs.extract_city_data(city_id)

        if 'error' in forecast_json or int(forecast_json['id']) != city_id:
            return 'Cidade ' + city_id.__str__() + ' nao encontrada', 400

    else:
        return 'Erro: Id informado invalido', 404

    try:
        fd.persist_city_data(forecast_json)
        return 'Cidade id: ' + city_id.__str__() + ' registrada com sucesso', 201

    except Exception as e:
        return f'Erro: {e}', 400


@forecast_controller.route("/analise", methods=["GET"])
def analise():
    initial_date = request.args['data_inicial']
    end_date = request.args['data_final']

    analise_jason = fd.retrieve_forecast_data(initial_date, end_date)

    json_data = json.dumps(analise_jason)
    return json_data, 200
