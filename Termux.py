from db2csv import itemWrite
import sys
import subprocess
import json
import datetime


class Termux:
    def __init_(self):
        pass

    def sensorStop(self):
        msg = subprocess.Popen(
            [
                "termux-sensor",
                "-c",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return msg

    def sensorStart(self, sensor, duration, job):
        delay = 10
        number = 1000 * int(duration) / delay
        msg = subprocess.Popen(
            [
                "termux-sensor",
                "-s",
                sensor,
                "-d",
                str(delay),
                "-n",
                str(int(round(number))),
            ],
            stdout=subprocess.PIPE,
        )
        lines = []
        data = []
        for line in msg.stdout:
            line = line.decode("UTF-8")
            line = line.replace(",", "").replace("\n", "")
            try:
                if float(line):
                    if len(lines) == 0:
                        lines.append(str(datetime.datetime.now()))
                    if len(lines) <= 5:
                        lines.append(line.replace(" ", ""))
                    if len(lines) == 4:
                        data.append(lines)
                        itemWrite().write(lines, ["timestamp", "x", "y", "z"], job)
                        lines = []
            except:
                pass
        return data

    def audioInfo(self):
        msg = subprocess.Popen(
            [
                "termux-audio-info",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return json.loads(msg)

    def tts(self, text):
        msg = subprocess.Popen(
            ["termux-tts-speak", text],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return msg

    def wake_lock(self):
        msg = subprocess.Popen(
            [
                "termux-wake-lock",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return

    def wake_unlock(self):
        msg = subprocess.Popen(
            [
                "termux-wake-unlock",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return

    def notification(self, text):
        msg = subprocess.Popen(
            ["termux-notification", "-c", text],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return

    def photo(self):
        filename = str(datetime.datetime.now())
        filename = (
            filename.replace(" ", "_")
            .replace(":", "")
            .replace("-", "")
            .replace(".", "")
        )
        msg = subprocess.Popen(
            ["termux-camera-photo", "../../storage/dcim/" + filename + ".jpg"],
            stdout=subprocess.PIPE,
        )
        return

    def vibrate(self, duration):
        msg = subprocess.Popen(
            [
                "termux-vibrate",
                "-fd",
                duration,
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return

    def toast(self, weight, text):
        msg = subprocess.Popen(
            ["termux-toast", "-g", weight, text],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return

    def location(self):
        data = subprocess.Popen(
            [
                "termux-location",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        try:
            return json.loads(data)
        except:
            print("No data")
            return None

    def micRecord(self, filename, duration, bitrate):
        record = subprocess.Popen(
            [
                "termux-microphone-record",
                "-l",
                str(duration),
                "-b",
                str(bitrate),
                "-f",
                filename,
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return

    def micInfo():
        mic_info = subprocess.Popen(
            [
                "termux-microphone-record",
                "-i",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        try:
            return json.loads(mic_info)
        except:
            return

    def micRecordStop(self):
        recordStop = subprocess.Popen(
            [
                "termux-microphone-record",
                "-q",
            ],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        return recordStop

    def wifiScan(self):
        scanInfo = subprocess.Popen(
            ["termux-wifi-scaninfo"],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        try:
            return json.loads(scanInfo)
        except:
            return None

    def Battery(self):
        battInfo = subprocess.Popen(
            ["termux-battery-status"],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        try:
            return json.loads(battInfo)
        except:
            pass

    def wifiInfo():
        Info = subprocess.Popen(
            ["termux-wifi-connectioninfo"],
            stdout=subprocess.PIPE,
        ).communicate()[0]
        try:
            return json.loads(Info)
        except:
            return
