import threading
import Termux as T
import time
from keys import Keys
import datetime
from db2csv import itemWrite, AverageCalc
import os
from epoch import E
import config

lock = threading.Lock()


class Scan:
    def __init__(self):
        self.options = {}
        print("module name:", __name__)
        print("parent process:", os.getppid())
        print("process id:", os.getpid())
        while True:
            print("SCANNING")
            self.run()
            time.sleep(config.wifi)

    def keyswitch(self, item):
        items = []
        keys = Keys().wifikeys
        self.options["column_list"] = ", ".join(keys)
        items.append(E().run())
        for i, key in enumerate(keys):
            try:
                items.append(item[key])
            except KeyError:
                items.append("")
            except TypeError:
                items.append(item[len(keys)])
        return items

    def run(self):
        self.options["job"] = "WifiScan"
        self.wifiscan = T.Termux().wifiScan()
        try:
            for idx, item in enumerate(self.wifiscan):
                items = self.keyswitch(item)
                itemWrite().write(
                    items, self.options["column_list"], self.options["job"]
                )
            print(len(self.wifiscan), "ITEMS")
        except:
            pass

        return
