import datetime
import time
from calendar import timegm


class E:
    def __init__(self):
        pass

    def run(self):
        now = str(datetime.datetime.now())
        now = now.split(".")[0]
        utc_time = time.strptime(now, "%Y-%m-%d %H:%M:%S")
        return timegm(utc_time)
