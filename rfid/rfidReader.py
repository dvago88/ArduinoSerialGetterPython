# import requests
# from serialReader.SerialReader import *
# from entities.DataEntity import *
# import json
# from rest.Post import *
# from rest.Get import *
#
# # import multitasking
#
#
# cola_de_estaciones = []
# dict_de_rfids = {}
#
#
# # @multitasking.task
# def llego_algo():
#     global ser
#     while True:
#         rfid = input()
#         token = login()
#         user_id = get_user_id_from_code(token, rfid)
#         if user_id != -1:
#             station_number = input()
#             if is_station_available(token, station_number):
#                 dict_de_rfids[station_number] = rfid
#                 cola_de_estaciones.append(station_number)
#
#             else:
#                 data_dict = get_data_entity_of_station(token, station_number)
#                 if rfid == data_dict["rfid"]:
#                     n = str(station_number * -1).encode("utf-8")
#                     ser.write(n)
#                     ser.write(b"\n")
#                 else:
#                     print("No tiene los permisos necesarios para abrir esta estación")
