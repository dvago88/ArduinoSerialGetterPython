import requests
from serialReader.SerialReader import *
from entities.DataEntity import *
import json
from rest.Post import *
from rest.Get import *
from rfid.rfidReader import *


multitasking.set_max_threads(10)


# http://docs.python-requests.org/en/latest/



if __name__ == '__main__':
    inicio()
    fin()
    # token = login()
    # print(get_data_of_station(token, 1))
    # post_station(token, "", 1)
    # print(get_data_of_station(token, 1))
