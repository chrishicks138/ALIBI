import config
import Termux as T
from db2csv import itemWrite
import time
import datetime
from State import State
import os
from epoch import E
import hashlib
import Scan as s
import record as r


class G:
    state = None

    def __init__(self):
        print("module name:", __name__)
        print("parent process:", os.getppid())
        print("process id:", os.getpid())
        self.default = 5
        while True:
            self.scan()
            time.sleep(self.default)

    def scan(self):
        items = []
        keys = []
        msg = T.Termux().location()
        if msg is not None:
            options = {}
            options["data"] = msg
            options["geo_list"] = (47.657249, -117.381247)
            speed = msg["speed"]

            if int(speed) > 0.0:
                print("SPEED:", speed, "TIME:", self.default)
                self.default = 30
            elif int(speed) > 0.9:
                print("SPEED:", speed, "TIME:", self.default)
                self.default = 2
            elif int(speed) == 0.0:
                print("SPEED:", speed, "TIME:", self.default)
                self.default = 30

            r.gpsDistance(options).distance(500)
            keys.append("Timestamp")
            items.append(E().run())
            for item in msg.values():
                items.append(item)
            for key in msg.keys():
                keys.append(key)
            itemWrite().write(items, keys, "GPS")
            return

        else:
            # s.Scan().run()
            state = False
            return None
