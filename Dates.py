import datetime
import time


class Days:
    def __init__(self):

        from calendar import timegm

        now = str(datetime.datetime.now())
        now = now.split(".")[0]
        utc_time = time.strptime(now, "%Y-%m-%d %H:%M:%S")
        self.stamp = timegm(utc_time)
        self.x = datetime.datetime.now()
        self.dtime = str(self.x).split(".")[0]
        self.ftime = self.dtime.replace(" ", "_")
        self.today = self.x.strftime("%m-%d")
        self.date = self.x.strftime("%m-%d-%Y")
        weekday = datetime.datetime.strptime(self.date, "%m-%d-%Y").weekday() + 1


class Now:
    def start(self):
        now = time.time_ns()
        return now

    def end(self):
        now = time.time_ns()
        return now

    def result(self):
        nanoseconds = self.end() - self.start()
        return abs(nanoseconds) / 1000


class Labels:
    def __init__(self):
        self.today_label = []

    def add_today_label(self, data):
        self.today_label.append(data)

    def delete(self):
        self.today_label = []

    def label_chooser(self):
        return self.today_label


labels = Labels()


class Comprehensions:
    d = [
        datetime.datetime.fromordinal(day).strftime("%m-%d")
        for day in range(
            datetime.datetime.toordinal(Days().x),
            datetime.datetime.toordinal(Days().x) + 365,
        )
    ]
    month = [
        datetime.datetime.fromordinal(day).strftime("%m-%d")
        for day in range(
            datetime.datetime.toordinal(Days().x) - 31,
            datetime.datetime.toordinal(Days().x),
        )
    ]
    fortyfive_days = [
        datetime.datetime.fromordinal(day).strftime("%m-%d")
        for day in range(
            datetime.datetime.toordinal(Days().x) - 45,
            datetime.datetime.toordinal(Days().x),
        )
    ]
    sixty_days = [
        datetime.datetime.fromordinal(day).strftime("%m-%d")
        for day in range(
            datetime.datetime.toordinal(Days().x) - 60,
            datetime.datetime.toordinal(Days().x),
        )
    ]
    biyearly = [
        datetime.datetime.fromordinal(day).strftime("%m-%d")
        for day in range(
            datetime.datetime.toordinal(Days().x) - 180,
            datetime.datetime.toordinal(Days().x),
        )
    ]
    week = [
        datetime.datetime.fromordinal(day).strftime("%m-%d")
        for day in range(
            datetime.datetime.toordinal(Days().x) - 7,
            datetime.datetime.toordinal(Days().x),
        )
    ]


class Dates:
    def __init__(self):
        self.ordinal = datetime.datetime.toordinal(Days().x)

    def span_length(self, span):
        week = 7
        if span == "1":
            week = week + 1
        if span == "2":
            week = week * 2
        if span == "3":
            week = week * 4
        if span == "4":
            week = week * 12
        if span == "5":
            week = week * 24
        return week

    def today_b(self, e):
        return e

    def today_e(self, e, span):
        # result = e + 90
        result = e + self.span_length(span)
        return result

    def date_selector(self, span):
        return [
            datetime.datetime.fromordinal(day).strftime("%m-%d")
            for day in range(
                datetime.datetime.toordinal(x),
                datetime.datetime.toordinal(x) + self.span_length(span),
            )
        ]
