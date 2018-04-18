import serial

from entities.DataEntity import *
from rest.Post import *
from rest.Get import *
from rfid.rfidReader import *
import random
import json
import threading

# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports


# ser = serialReader.Serial('/dev/ttyACM0', 9600)

test_lock = threading.Lock()
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
        data_array = incoming_data[1:].split("/")
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
            ran = random.choice(cola_de_estaciones)
            n = str(ran).encode("utf-8")
            ser.write(n)  # corregier esto, debe enviarse n
            ser.write(b"\n")
            cola_de_estaciones.remove(ran)
            print("Cola de estaciones tiene {} valores".format(len(cola_de_estaciones)))
    else:
        print("Se recibió esto: {}".format(incoming_data[1:]))


def updata_stations_in_arduino():
    for key in dict_de_estaciones:
        if dict_de_estaciones[key]:
            n = str(key).encode("utf-8")
            ser.write(n)  # abrir la numero key
            ser.write(b"\n")
        else:
            n = str(key).encode("utf-8")
            ser.write(n)  # cerrar la numero key
            ser.write(b"\n")


def update_stations_dict_from_server():
    array_of_stations = json.loads(get_stations())

    for station in array_of_stations:
        dict_de_estaciones[station["id"]] = station["available"]


# ----------------------------------------------------------
# -                    RFID READER                         -
# ----------------------------------------------------------

cola_de_estaciones = []
dict_de_rfids = {}


def llego_algo():
    global ser
    while True:
        rfid = input()
        token = login()
        user_id = get_user_id_from_code(token, rfid)
        if user_id != -1:
            station_number = input()
            if is_station_available(token, station_number):
                dict_de_rfids[station_number] = rfid
                cola_de_estaciones.append(station_number)
            else:
                data_dict = get_data_entity_of_station(token, station_number)
                if rfid == data_dict["rfid"]:
                    n = str(int(station_number) * -1).encode("utf-8")
                    ser.write(n)
                    ser.write(b"\n")
                else:
                    print("No tiene los permisos necesarios para abrir esta estación")
        else:
            print("No eres un usuario registrado")
