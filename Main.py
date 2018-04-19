# import requests
from serialReader.SerialReader import *
# from entities.DataEntity import *
# import json
# from rest.Post import *
# from rest.Get import *
# from rfid.rfidReader import *
import subprocess
import time

from threading import Thread


# http://docs.python-requests.org/en/latest/

#def leer_rfid():
    #while True:
        #result = subprocess.Popen(["python", "Read.py"], stdout=subprocess.PIPE)
        #output, error = result.communicate()
        #print("error: {}".format(error))
        #print("output: {}".format(output.decode("utf-8")))
        #time.sleep(3)

def inicio():
    t1 = Thread(target=llego_algo)
    t2 = Thread(target=readSerial)
    #t3 = Thread(target=leer_rfid)

    t1.start()
    t2.start()
    #t3.start()
    print("Inicio completado")


if __name__ == '__main__':
    inicio()

