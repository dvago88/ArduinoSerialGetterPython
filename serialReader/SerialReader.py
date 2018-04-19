import serial

from entities.DataEntity import *
from rest.Post import *
from rest.Get import *
from rfid.rfidReader import *
import json
import subprocess
import time
import RPi.GPIO as GPIO

# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports


ser = serial.Serial('/dev/ttyACM0', 9600)
# ser = serial.Serial('COM5', 9600)
dict_de_estaciones = {}
GPIO.setmode(GPIO.BCM)

MATRIX = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12],
          [13, 14, 15, 16]]

ROW = [4, 14, 15, 17]
COL = [18, 27, 22, 23]
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)


# ----------------------------------------------------------
# -                    SERIAL READER                       -
# ----------------------------------------------------------

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
        s = incoming_data[1]
        try:
            i = cola_de_estaciones.index(s)
            n = str(s).encode("utf-8")
            ser.write(n)
            ser.write(b"\n")
            cola_de_estaciones.remove(s)
            print("Cola de estaciones tiene {} valores".format(len(cola_de_estaciones)))
        except:
            print("Estación {} no ha sido solicitada aun".format(s))
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
# -                    PAD READER                          -
# ----------------------------------------------------------        

def read_number_from_pad():
    try:
        while (True):
            for j in range(4):
                GPIO.output(COL[j], 0)
                for i in range(4):
                    if GPIO.input(ROW[i]) == 0:
                        print(MATRIX[i][j])
                        return MATRIX[i][j]

                GPIO.output(COL[j], 1)
    except KeyboardInterrupt:
        GPIO.cleanup()


# ----------------------------------------------------------
# -                    RFID READER                         -
# ----------------------------------------------------------

cola_de_estaciones = []
dict_de_rfids = {}


def llego_algo():
    global ser
    while True:
        result = subprocess.Popen(["python", "Read.py"], stdout=subprocess.PIPE)
        output, error = result.communicate()
        rfid = str(int(output.decode("utf-8")))
        print(rfid)
        token = login()
        user_id = get_user_id_from_code(token, rfid)
        if int(user_id) != -1:
            station_number = str(read_number_from_pad())
            print("Estación numero {} solicitada".format(station_number))
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
            time.sleep(2)
