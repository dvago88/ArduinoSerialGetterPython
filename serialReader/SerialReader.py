import serial

from entities.DataEntity import *
from rest.Post import *
from rest.Get import *
import json
import subprocess
import time
import RPi.GPIO as GPIO
import lcddriver

# https://pythonhosted.org/pyserial/shortintro.html#opening-serial-ports


ser = serial.Serial('/dev/ttyACM0', 9600)
# ser = serial.Serial('COM5', 9600)
lcd = lcddriver.lcd()
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
# -                    LCD WRITER                          -
# ----------------------------------------------------------

def write_to_lcd(arriba,abajo):
    lcd.lcd_clear()
    lcd.lcd_display_string(arriba,1)
    lcd.lcd_display_string(abajo,2)

# ----------------------------------------------------------
# -                    SERIAL READER                       -
# ----------------------------------------------------------

def readSerial():
    token = login()
    while True:
        try:
            state = ser.readline()
            print(state.decode("utf-8"))
            return_serial_data(state.decode("utf-8"), token)
        except:
            pass


def return_serial_data(incoming_data, token):
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
        post_historial(token, data_entity.toJson())
        post_station(token, "", station_number)
        write_to_lcd("Estación # {}".format(station_number),"cerrada")
    elif incoming_data[0] == 'b':
        s = incoming_data[1]
        try:
            i = cola_de_estaciones.index(s)
            n = str(s).encode("utf-8")
            ser.write(n)
            ser.write(b"\n")
            cola_de_estaciones.remove(s)
            print("Cola de estaciones tiene {} valores".format(len(cola_de_estaciones)))
            #write_to_lcd("Cola de estaciones","tiene {} valores".format(len(cola_de_estaciones)))
        except:
            print("Estación {} no ha sido solicitada aun".format(s))
            write_to_lcd("Estacion {} no ha".format(s),"sido solicitada aun".format(len(cola_de_estaciones)))

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
    token = login()
    while True:
        result = subprocess.Popen(["python", "Read.py"], stdout=subprocess.PIPE)
        output, error = result.communicate()
        try:
            rfid = str(int(output.decode("utf-8")))
        except ValueError as v:
            print(v)
            print("Hubo un penoso error, intenta de nuevo")
            write_to_lcd("Hubo un error","intenta de nuevo")
            rfid = 0000000
        print(rfid)        
        user_dict = get_user_id_from_code(token, rfid)
        if int(user_dict["id"]) != -1:
            write_to_lcd("Bienvenid@:",user_dict["primerNombre"])
            station_number = str(read_number_from_pad())
            print("Estación numero {} solicitada".format(station_number))
            write_to_lcd("Estacion # {}".format(station_number),"solicitada")
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
                    write_to_lcd("Accesso denegado","Reportando...")
        else:
            print("No eres un usuario registrado")
            write_to_lcd("Usuario invalido","LADRON!!")
            time.sleep(2)


