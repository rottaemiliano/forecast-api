import sqlite3


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("resources/sqlite/database.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


class ForecastDAO():
    def __init__(self):
        print("__instance created")

    def persist_city_data(json):
        conn = db_connection()
        cursor = conn.cursor()

        city_id = json['id']
        city_name = json['name']
        state = json['state']
        country = json['country']

        sql = """INSERT OR REPLACE INTO city (id, city_name, state, country) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (city_id, city_name, state, country))

        for forecast_data in json['data']:
            forecast_date = forecast_data['date']
            probability = forecast_data['rain']['probability']
            precipitation = forecast_data['rain']['precipitation']
            temperature_min = forecast_data['temperature']['min']
            temperature_max = forecast_data['temperature']['max']
            sql = """INSERT OR REPLACE INTO forecast_data (city_id, forecast_date, probability, precipitation, temperature_min, temperature_max)
                                      VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (city_id, forecast_date, probability, precipitation, temperature_min, temperature_max))

        conn.commit()

    def retrieve_forecast_data(initial_date, end_date):
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
        if rows:
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

        if rows:
            analise_jason['average_precipitation'] = []
            for row in rows:
                analise_jason['average_precipitation'].append({"city_id": row[0], "avg": row[1]})

                return analise_jason


fd = ForecastDAO()
