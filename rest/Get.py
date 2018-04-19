import requests
import json

# baseUrl = "http://localhost:8090/"
baseUrl = "https://aqueous-temple-46001.herokuapp.com/"


def get_stations():
    r = requests.get(baseUrl + "stations")
    return r.text


def get_data_entity_of_station(token, station_id):
    return json.loads(get_request_base(token, str(station_id)).text)


def get_user_id_from_code(token, rifd):
    return get_request_base(token, "user/code/" + str(rifd)).text


def is_station_available(token, station_id):
    dict_res = json.loads(get_request_base(token, "stations/" + str(station_id)).text)
    return dict_res["available"]


def get_request_base(token, variable):
    headers = {
        "Authentication": "Bearer " + token,
        "Authorization": "raspberry"
    }
    url = baseUrl + variable
    res = requests.get(url, headers=headers)
    return res
