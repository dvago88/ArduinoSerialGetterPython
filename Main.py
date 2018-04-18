# import requests
from serialReader.SerialReader import *
# from entities.DataEntity import *
# import json
# from rest.Post import *
# from rest.Get import *
# from rfid.rfidReader import *

from threading import Thread


# http://docs.python-requests.org/en/latest/


def inicio():
    t1 = Thread(target=llego_algo)
    t2 = Thread(target=readSerial)

    t1.start()
    t2.start()
    print("Inicio completado")


if __name__ == '__main__':
    inicio()

