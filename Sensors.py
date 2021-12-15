import config
import threading
import time
import Termux as T
from State import State
from keys import Keys
from db2csv import AverageCalc
import os

lock = threading.Lock()


class Sensors:
    def __init__(self):
        while True:
            self.options = {}
            self.start_scan()
            time.sleep(config.sensors)

    def start_scan(self):
        self.options["sensor"] = "PS ALS"
        self.options["job"] = "LightSensor"
        self.options["duration"] = config.sensors
        self.options["length"] = config.sensors
        self.options["column_list"] = "Timestamp, Value"
        lock.acquire()
        l = threading.Thread(target=self.sensorBMI160())
        l.start()
        l.join()
        lock.release()
        self.options["sensor"] = "Linear Acceleration"
        self.options["job"] = "Accelerometer"
        self.options["column_list"] = ", ".join(Keys().sensorkeys)
        lock.acquire()
        s = threading.Thread(target=self.sensorBMI160())
        s.start()
        s.join()
        lock.release()
        lock.acquire()
        self.options["sensor"] = "QMC6308"
        self.options["job"] = "Magnetometer"
        s = threading.Thread(target=self.sensorBMI160())
        s.start()
        s.join()
        lock.release()

    def sensorBMI160(self):
        msg = T.Termux().sensorStart(
            self.options["sensor"],
            self.options["length"],
            self.options["job"],
        )
        T.Termux().sensorStop()
        #  if msg is not None:
        #      if self.options['job'] == 'Accelerometer':
        #  avg = AverageCalc().average(msg)
        #  print(avg)
