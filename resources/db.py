import sqlite3

conn = sqlite3.connect("resources/sqlite/database.sqlite")

cursor = conn.cursor()
sql_create_city = """ 
CREATE TABLE city (
    id integer PRIMARY KEY,
    city_name text NOT NULL,
    state text NOT NULL,
    country text NOT NULL 
)
"""

sql_create_forecast_data = """ 
CREATE TABLE forecast_data (
    id integer PRIMARY KEY AUTOINCREMENT,
    city_id integer NOT NULL,
    forecast_date date NOT NULL,
    probability integer,
    precipitation integer,
    temperature_min integer,
    temperature_max integer,
    FOREIGN KEY(city_id) REFERENCES city(id)
)
"""
cursor.execute(sql_create_city)
cursor.execute(sql_create_forecast_data)
