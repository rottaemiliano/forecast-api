import json
import sqlite3

import requests
from flask import Flask, request, json
from forecast import app

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("../resources/sqlite/database.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


def extract_city_data(cityid: int):
    url: str = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/'
    url += cityid.__str__()
    url += '/days/15?token=b22460a8b91ac5f1d48f5b7029891b53'

    req = requests.get(url)
    return req.json()


def persist_city_data(json):
    conn = db_connection()
    cursor = conn.cursor()

    city_id = json['id']
    city_name = json['name']
    state = json['state']
    country = json['country']
    sql = """INSERT INTO city (id, city_name, state, country) VALUES (?, ?, ?, ?)"""
    cursor.execute(sql, (city_id, city_name, state, country))

    for forecast_data in json['data']:
        forecast_date = forecast_data['date']
        probability = forecast_data['rain']['probability']
        precipitation = forecast_data['rain']['precipitation']
        temperature_min = forecast_data['temperature']['min']
        temperature_max = forecast_data['temperature']['max']
        sql = """INSERT INTO forecast_data (city_id, forecast_date, probability, precipitation, temperature_min, temperature_max)
                                  VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(sql, (city_id, forecast_date, probability, precipitation, temperature_min, temperature_max))

    conn.commit()


@app.route('/cidade', methods=['POST'])
def cidade():
    if 'id' in request.args:
        city_id = int(request.args['id'])
        forecast_json = extract_city_data(city_id)

        if 'error' in forecast_json or int(forecast_json['id']) != city_id:
            return 'City ' + city_id.__str__() + ' nao encontrada', 404

    else:
        return 'Erro: Id informado invalido', 404

    try:
        persist_city_data(forecast_json)
        return 'Cidade id: ' + city_id.__str__() + ' registrada com sucesso', 201

    except Exception as e:
        return f'Erro: {e}', 422

@app.route("/analise", methods=["GET"])
def analise():
    initial_date = request.args['data_inicial']
    end_date = request.args['data_final']

    analise_jason = {}


    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT c.id, "
                   "c.city_name, "
                   "f.temperature_max "
                   "FROM forecast_data f, city c "
                   "WHERE c.id = f.city_id "
                   "AND f.forecast_date >= ? "
                   "AND f.forecast_date <= ? "
                   "ORDER BY f.temperature_max DESC, c.city_name",
                   (initial_date, end_date))

    rows = cursor.fetchall()
    if rows != []:
        analise_jason['max_temperature_city_id'] = rows[0][0]
        analise_jason['max_temperature_city_name'] = rows[0][1]

    cursor.execute("SELECT city_id, "
                   "ROUND(AVG(precipitation), 2) "
                   "FROM forecast_data "
                   "WHERE forecast_date >= ? "
                   "AND forecast_date <= ? "
                   "GROUP BY city_id",
                   (initial_date, end_date))

    rows = cursor.fetchall()

    if rows != []:
        analise_jason['average_precipitation'] = []
        for row in rows:
            analise_jason['average_precipitation'].append({"city_id": row[0], "avg": row[1]})

    json_data = json.dumps(analise_jason)
    return json_data, 200

