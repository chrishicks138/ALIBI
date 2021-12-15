import datetime
import time
import Termux as T

class C():
    def __init__(self):
        T.Termux().photo()
        print(str(datetime.datetime.now()), 'JOB C FINISHED')
        time.sleep(10)

