from db2csv import itemWrite
from Termux import Termux as T
import time
from db2csv import itemWrite
import os


class N:
    def __init__(self):

        print("module name:", __name__)
        print("parent process:", os.getppid())
        print("process id:", os.getpid())
        while True:
            columns = []
            items = []
            data = T.wifiInfo()
            values = data.values()
            keys = data.keys()
            for idx, k in enumerate(keys):
                columns.append(k)
                items.append(data[k])
                if k == "ip":
                    ip = data[k]
                    ip = ip.split(".")
                    ip = ".".join(ip[0:3])

                    import sub as Sub

                    try:
                        pass
                        # Sub.Sub().nMap(ip + ".0./24")
                    except Exception as e:
                        print(e)
                if k == "supplicant_state":
                    print(data[k])
                if data[k] == "COMPLETED":
                    print(k, data[k])

                job = "NET"
                itemWrite().write(items, columns, job)
                time.sleep(config.netcheck)
