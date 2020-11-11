import sqlite3

from flask import json, Flask, request

forecast_api = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("resources/sqlite/database.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


def extract_city_data(cityid: int):
    url: str = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/'
    url += cityid
    url += '/days/15?token=b22460a8b91ac5f1d48f5b7029891b53'

    data = request.urlopen(url)
    forecast_data = json.loads(data)

    return forecast_data

def persist_city_data(data : json):
    conn = db_connection()
    cursor = conn.cursor()

    new_author = data.form["author"]
    new_lang = request.form["language"]
    new_title = request.form["title"]
    sql = """INSERT INTO city (author, language, title)
                      VALUES (?, ?, ?)"""
    cursor.execute(sql, (new_author, new_lang, new_title))
    conn.commit()


@forecast_api.route('/cidade', method=['POST'])
def cidade():

    id = request.args['id']

    forecast_data = extract_city_data(id)
    if forecast_data['id'] != id:
        return 'City ' + id + ' nao encontrada', 404

    return forecast_data, 200

    persist_city_data(forecast_data)

    return 'Cidade id: ' + id + ' registrada com sucesso', 201

# @app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
# def single_book(id):
#     conn = db_connection()
#     cursor = conn.cursor()
#     book = None
#     if request.method == "GET":
#         cursor.execute("SELECT * FROM book WHERE id=?", (id,))
#         rows = cursor.fetchall()
#         for r in rows:
#             book = r
#         if book is not None:
#             return jsonify(book), 200
#         else:
#             return "Something wrong", 404
#
#     if request.method == "PUT":
#         sql = """UPDATE book
#                  SET title=?,
#                      author=?,
#                      language=?
#                  WHERE id=? """
#
#         author = request.form["author"]
#         language = request.form["language"]
#         title = request.form["title"]
#         updated_book = {
#             "id": id,
#             "author": author,
#             "language": language,
#             "title": title,
#         }
#         conn.execute(sql, (author, language, title, id))
#         conn.commit()
#         return jsonify(updated_book)
#
#     if request.method == "DELETE":
#         sql = """ DELETE FROM book WHERE id=? """
#         conn.execute(sql, (id,))
#         conn.commit()
#         return "The book with id: {} has been ddeleted.".format(id), 200
