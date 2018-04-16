import serial

from entities.DataEntity import DataEntity
from rest.Post import *
from rest.Get import *
from rfid.rfidReader import *
import random
import json
import multitasking

# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports


# ser = serialReader.Serial('/dev/ttyACM0', 9600)


ser = serial.Serial('COM3', 9600)
dict_de_estaciones = {}


def readSerial():
    while True:
        try:
            state = ser.readline()
            print(state.decode("utf-8"))
            return_serial_data(state.decode("utf-8"))
        except:
            pass


def return_serial_data(incoming_data):
    if incoming_data[0] == 'a':
        data_array = incoming_data.split("/")
        station_number = data_array[0]
        rfid = dict_de_rfids[station_number]

        data_entity = DataEntity(
            station_number,
            data_array[1],
            data_array[2],
            data_array[3],
            rfid,
        )
        token = login()
        post_historial(token, data_entity.toJson())
        post_station(token, "", station_number)
    elif incoming_data[0] == 'b':
        # Por ahora es aleatorio pero cuando sea real los sensores dirán cual estación es
        if len(cola_de_estaciones) > 0:
            n = random.choice(cola_de_estaciones)
            ser.write(b"\n")  # corregier esto, debe enviarse n
    else:
        print("Se recibió esto: {}".format(incoming_data[1:]))


def updata_stations_in_arduino():
    for key in dict_de_estaciones:
        if dict_de_estaciones[key]:
            print(b"")
            ser.write(b"\n")  # abrir la numero key
        else:
            ser.write(b"\n")  # cerrar la numero key


def update_stations_dict_from_server():
    array_of_stations = json.loads(get_stations())

    for station in array_of_stations:
        dict_de_estaciones[station["id"]] = station["available"]
