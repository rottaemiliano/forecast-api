import requests


class ForecastService():

    def __init__(self):
        print("__instance created")

    def extract_city_data(cityid: int):
        url: str = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/'
        url += cityid.__str__()
        url += '/days/15?token=b22460a8b91ac5f1d48f5b7029891b53'

        req = requests.get(url)
        return req.json()


fs = ForecastService()
