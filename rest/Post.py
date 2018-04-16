import requests
from serialReader.SerialReader import *
from entities.DataEntity import *
import json

# http://docs.python-requests.org/en/latest/
baseUrl = "http://localhost:8090/"

def login():
    credentials = (('username', 'raspberry'), ('password', 'raspberry'))
    res = requests.post('http://localhost:8090/perform_login', data=credentials)
    dictToken = json.loads(res.text)
    token = dictToken["jws"]
    return token


def post_data_entity(token, data):
    return post_base(token, data, "")


def post_historial(token, data):
    return post_base(token, data, "historial/")


def post_station(token, data, station_number):
    return post_base(token, data, "stations/" + str(station_number))


def post_base(token, data, url_complement):
    url = baseUrl + url_complement
    headers = {
        "Authentication": "Bearer " + token,
        "Authorization": "raspberry",
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=headers, data=data)
    return res.text
