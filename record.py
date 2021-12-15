import time
import math
from Termux import Termux


class Range:
    pass


class gpsDistance:
    def __init__(self, options):
        self.options = options
        self.lat = float(self.options["data"]["latitude"])
        self.lon = float(self.options["data"]["longitude"])

    def range_compare(self, *args):
        diff_lat = args[0]
        diff_lon = args[1]
        distance = args[2]
        print("DISTANCE", round(int(distance) * 3.1 / 5280, 2), "MILES")
        limit = args[3]
        if distance < limit:
            self.options["inRange"] = True
            print("In Range:", self.options["inRange"])
            Range.inRange = True
            Range.diff_lat = diff_lat
            Range.diff_lon = diff_lon
            Range.distance = distance

        else:
            self.options["inRange"] = False
            print("In Range:", self.options["inRange"])
            Range.inRange = False
            Range.diff_lat = diff_lat
            Range.diff_lon = diff_lon
            Range.distance = distance

    def distance(self, limit):
        item = self.options["geo_list"]
        db_lat = float(item[0])
        db_lon = float(item[1])
        diff_lat = db_lat - self.lat
        diff_lon = db_lon - self.lon
        hav_lat = self.lat * math.pi / 180
        hav_lon = self.lon * math.pi / 180
        hav_lat2 = db_lat * math.pi / 180
        hav_lon2 = db_lon * math.pi / 180
        hav_diff_lat = diff_lat * math.pi / 180
        hav_diff_lon = diff_lon * math.pi / 180
        R = 6371 * 1000
        a = math.sin(hav_diff_lat / 2) * math.sin(hav_diff_lat / 2) + math.cos(
            hav_lat
        ) * math.cos(hav_lat2) * math.sin(hav_diff_lon / 2) * math.sin(hav_diff_lon / 2)
        c = 2 * math.atan2(math.radians(math.sqrt(a)), math.radians(math.sqrt(1 - a)))
        distance = R * c
        self.range_compare(diff_lat, diff_lon, distance, limit)
