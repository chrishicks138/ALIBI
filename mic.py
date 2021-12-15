import Termux as T
import config
from Dates import Days
import os
import datetime
import time
import threading


class Microphone:
    def __init__(self):
        print("module name:", __name__)
        print("parent process:", os.getppid())
        print("process id:", os.getpid())
        while True:
            self.run()
            time.sleep(config.dircheck)

    def run(self):
        self.options = {}
        self.options["duration"] = str(1800)
        self.options["sdcard"] = False
        self.options["bitrate"] = 96000
        self.info = T.Termux.micInfo()
        time.sleep(1)
        base = "/storage/emulated/0"
        sdcard = "/storage/4220-0353"
        if self.options["sdcard"]:
            base = sdcard
        root = "Recordings"
        if self.info["isRecording"] == None:
            return
        elif self.info["isRecording"] == False:
            if root not in os.listdir(base):
                print(root, "not found, creating", base + "/" + root)
                os.makedirs(base + "/" + root)
            if Days().today not in os.listdir(base + "/" + root):
                print(
                    Days().today,
                    "not found, creating",
                    base + "/" + root + "/" + Days().today,
                )
                os.makedirs(base + "/" + root + "/" + Days().today)
            print("Activating")
            bitrate = str(self.options["bitrate"])
            self.options["location"] = (
                base
                + "/"
                + root
                + "/"
                + Days().today
                + "/Audio_"
                + str(datetime.datetime.now())
                + ".m4a"
            )
            T.Termux().micRecord(
                self.options["location"],
                self.options["duration"],
                self.options["bitrate"],
            )
        else:
            return
