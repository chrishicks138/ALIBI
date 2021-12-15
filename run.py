from multiprocessing import Process
import threading
import time
import os
from State import State
import gps
import batt
import mic
import Scan as S
import Sensors as SE
import net


def f(q):
    b = Process(
        target=batt.B,
    )
    b.start()
    time.sleep(1)
    m = Process(target=mic.Microphone)
    m.start()
    time.sleep(1)
    g = Process(target=gps.G)
    g.start()
    time.sleep(1)
    sc = threading.Thread(target=SE.Sensors)
    sc.start()
    time.sleep(1)
    scan = threading.Thread(target=S.Scan)
    scan.start()


if __name__ == "__main__":
    f("main line")
