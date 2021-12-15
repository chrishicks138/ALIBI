import datetime
import time
import config
import Termux as T
from db2csv import itemWrite
from State import State
import os


class B:
    def __init__(self):
        print("module name:", __name__)

        print("parent process:", os.getppid())
        print("process id:", os.getpid())
        while True:
            self.run()

    def run(self):
        State.discharging = None
        items = []
        msg = T.Termux().Battery()
        columns = list(msg.keys())
        for i, item in enumerate(msg.values()):
            items.append(item)
        itemWrite().write(items, columns, "Battery")
        if items[3] == "DISCHARGING":
            State.discharging = True
        else:
            State.discharging = False
        time.sleep(config.battery)
