import time
import json


class DataEntity:

    def __init__(self, stationNumber, sensor2, sensor3, sensor4, rfid):
        self.stationNumber = stationNumber
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.sensor4 = sensor4
        self.rfid = rfid
        self.timeInSeconds = int(time.time() * 1000)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
