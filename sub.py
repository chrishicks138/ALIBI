import subprocess


class Sub:
    def __init_(self):
        pass

    def nMa(self, ip):
        msg = subprocess.Popen(
            [
                "nmap",
                "-sn",
                ip,
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return msg

    def nMap(self, ip):
        msg = subprocess.Popen(
            [
                "nmap",
                "-v",
                "-sn",
                ip,
            ],
            stdout=subprocess.PIPE,
        )
        lines = []
        data = []
        for line in msg.stdout:
            line = line.decode("UTF-8")
            line = line.replace(",", "").replace("\n", "")
            print(line)
        return data
