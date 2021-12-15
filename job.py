import time
import record
from Termux import Termux
import sqlConfig
import sql
import threading
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
import ast
import os
from app.Dates import  Dates, Days, Comprehensions
from db2csv import itemWrite, AverageCalc



class Notify():
    def __init__(self, options):
        import app.Dates as Dates
        self.options = options
        #self.status = options['status']
        #self.status_type = options['status_type']
        Dates.Now().end()
        end = round(Dates.Now().result())
        self.fixed_sleep = int(self.options['length']) - end
        self.processing_time = str(end)
        pass

    def notify(self):
        self.status_type = "vibrate"
        if self.options['range'] == True:
            self.args = ' In Range: '+str(record.Range().inRange)+', '+str(round(record.Range().distance, 3))+' meters.'
        self.total_time = int(self.options['duration']) * (int(self.processing_time) + self.fixed_sleep)
        if self.status_type == "toast":
            self.args = "Iteration: "+str(self.options['iteration'])+'/'+str(self.options['max_iter'])+" Sleep is:"+str(self.fixed_sleep)+" seconds. Processing time is "+self.processing_time+" seconds. Total estimated time: "+str(self.total_time / 60 )+' minutes.'
            Termux().toast('bottom', self.args)
        elif self.status_type == "vibrate":
            self.args = str(10)
            Termux().vibrate(self.args)
        elif self.status_type == "tts":
            self.args = "Iteration: "+self.options['iteration']+" of "+self.options['max_iter']+" Number of access points: "+str(self.options['scan_len'])
            if self.options['withSet'] == "BT":
                audio_info = Termux().audioInfo()
                if audio_info['BLUETOOTH_A2DP_IS_ON']:
                    Termux().tts(self.args)
        elif self.status_type == "notification":
            Termux().notification(self.args)


class Options():
    def __init__(self, options):
        self.option = options
        self.options = {}
        for option in self.option:
            self.options[option] = self.option[option]
            params = [
                    'db',
                    'range',
                    'range_options',
                    'status',
                    'isScan',
                    'isCombo',
                    'isLoop',
                    'sdcard',

                    ]
            for param in params:
                if option == param:
                    self.type_conv(option)
            
            if option == 'status_args':
                self.options[option] = int(self.option[option])
            if option == 'duration':
               self.options[option] = int(self.option[option])
            if option == 'length':
                self.options[option] = int(self.option[option])
        if 'Mic' in self.options['job']:
            if self.options['duration'] == 1:
                self.options['duration'] = 900
            if self.options['duration'] == 2:
                self.options['duration'] = 1800
            if self.options['duration'] == 3:
                self.options['duration'] = 3600
            if self.options['duration'] == 4:
                self.options['duration'] = 21600
            Logger("Duration: "+str(self.options['duration']))
            while True:
                s = threading.Thread(target=self.mic)
                s.start()
        if "cam" in self.options['job']:
            self.duration = int(self.options['duration'])
            self.length = int(self.options['length'])
            self.options = options
            for i in range(self.duration):
                s = threading.Thread(target=self.photo)
                s.start()
                time.sleep(2)
        if "GPS" in self.options['job']:
            self.isScan = self.options['isScan']
            if self.isScan:
                if self.options['range_option'] is not False:
                    self.feet = self.limit
                    if self.feet == '1':
                        self.feet = '50'
                    self.limit = 0.305 * self.feet
                    rangeDetect(self.options).scan()
        if self.options['db'] == True:
            try:
                self.duration = int(self.options['duration'])
                self.length = int(self.options['length'])
            except:
                pass
            Logger("DB init")
            self.options['isLoop'] = True
            self.db_file = self.options['db_file']
            self.options['running'] = False 
            Db().options(self.options)

    def type_conv(self, option):
        if self.options[option] == 'True':
            self.options[option] = True
        else:
            self.options[option] = False

    def mic(self):
        self.info = Termux.micInfo()
        base = "/storage/emulated/0"
        sdcard = "/storage/4220-0353"
        if self.options['sdcard']:
            base = sdcard
        root = "Recordings"
        if self.info['isRecording'] == False:
            Logger("Mic activating")
            import app.Dates as Dates
            if root not in os.listdir(base):
                print(root, "not found, creating", base+"/"+root)
                os.makedirs(base+"/"+root)
            if Days().today not in os.listdir(base+"/"+root):
                print(Days().today, "not found, creating", base+"/"+root+"/"+Days().today)
                os.makedirs(base+"/"+root+"/"+Days().today)
            Logger("Setting location")
            self.options['bitrate'] = '96'
            bitrate = self.options['bitrate']
            self.options['location'] = base+"/"+root+"/"+Days().today+"/Audio_"+bitrate+str(datetime.datetime.now())+".m4a"
            Logger(self.options['location'])
            Logger("Not recording, starting...")
            Termux().micRecord(self.options['location'],self.options['duration'], self.options['bitrate'])
        else:
            Logger("Active: "+str(self.info['isRecording'])+' '+"Duration:"+' '+str(self.options['duration']))
        time.sleep(10)

    def photo(self):
        Logger('Camera executed')
        Termux().photo(self.options['cam'])

class Scan():
    def __init__(self):
        pass

    def scan(self):
        self.options = {}
        print("Starting scan")
        try:
            self.gpsscan = Termux().location()
            print("SPEED", self.gpsscan['speed'])
            self.start_scan()
        except:
            print("Unable to get GPS fix")
            pass

    def start_scan(self):
        if self.gpsscan['speed'] > 1:
            self.options['sensor'] = 'Linear Acceleration'
            self.options['job'] = "Accelerometer"
            self.options['duration'] = 2
            self.options['length'] = 30
            self.options['column_list'] = ', '.join(Db().sensorkeys)
            t = threading.Thread(target=self.sensorBMI160)
            t.start()

        elif self.gpsscan['speed'] < 1:
            self.options['sensor'] = 'QMC6308'
            self.options['job'] = "Magnetometer"
            self.options['duration'] = 2
            self.options['length'] = 30
            self.options['column_list'] = ', '.join(Db().sensorkeys)
            t = threading.Thread(target=self.sensorBMI160)
            t.start()
        time.sleep(60)

    def sensorBMI160(self):
        Logger(self.options['job']+" starting...")
        Logger("DURATION: "+str(self.options['length']))
        msg = Termux().sensorStart(self.options['sensor'], self.options['length'])
        Logger(" Parsing "+self.options['job'])
        self.sensorParse(msg)
        #p = threading.Thread(target=self.sensorParse, args=(msg,))
        #p.start()
        #p.join()

    def sensorParse(self, msg):
        msg_data = msg.decode("UTF-8")
        data = msg_data.split(': [')
        data = [item.replace(']', '') for item in data]
        data = [item.replace('}', '') for item in data]
        data = [item.replace('{', '') for item in data]
        
        if self.options['sensor'] == 'QMC6308':
            data = [item.replace('"QMC6308 QMC6308":', '') for item in data]
        #  if self.options['job'] == 'Accelerometer':
        #      data = [item.replace('"BMI160 Accelerometer":', '') for item in data]
        if self.options['sensor'] == 'Linear Acceleration':
            data = [item.replace('"Linear Acceleration":', '') for item in data]
        
        data = [item.replace('"values"', '') for item in data]
        data = [item.replace('\n', '') for item in data]
        data = [item.replace(' ', '') for item in data]
        for i, unit in enumerate(data):
            now = datetime.datetime.now()
            self.item = []
            unit = unit.split(',')
            if len(unit) > 2:
                self.item.append(str(now))
                self.item.append(unit[0])
                self.item.append(unit[1])
                self.item.append(unit[2])
                itemWrite().write(self.item, self.options['column_list'], self.options['job'])
        avg = AverageCalc().average(data)
        print(avg)
        if self.options['job'] == "Accelerometer":
            if avg > 0.01:
                self.options['sensor'] = 'Linear Acceleration'
                self.options['job'] = "Accelerometer"
                self.options['duration'] = 2
                self.options['length'] = 60
                self.sensorBMI160()
            else:
                self.options['sensor'] = 'QMC6308'
                self.options['job'] = "Magnetometer"
                self.options['duration'] = 2
                self.options['length'] = 60
                self.sensorBMI160()
                #  pass
        Logger("Data length: "+str(len(data)))
        Termux().sensorStop()
        Logger(self.options['job']+' '+str(datetime.datetime.now())+" Finished")


class Logger():
    def __init__(self, log):
        self.msg = log
        self.log()

    def log(self):
        file = './logger.log'
        with open(file, 'a') as log:
            log.write(str(datetime.datetime.now())+' '+self.msg+"\n")
            log.close()
        print(self.msg)        


Logger('\nApplication initialization\n')


class ThreadStart(threading.Thread):

    def __init__(self, options):
        super(ThreadStart, self).__init__()
        self.options = options
        self.db_file = options['db_file']
        self.scan_worker()

    def sensorBMI160(self):
        Logger(self.options['job']+" starting...")
        Logger("DURATION: "+str(self.options['length']))
        msg = Termux().sensorStart(self.options['sensor'], self.options['length'])
        Logger(" Parsing "+self.options['job'])
        self.sensorParse(msg)
        #p = threading.Thread(target=self.sensorParse, args=(msg,))
        #p.start()
        #p.join()

    def sensorParse(self, msg):
        msg_data = msg.decode("UTF-8")
        data = msg_data.split(': [')
        data = [item.replace(']', '') for item in data]
        data = [item.replace('}', '') for item in data]
        data = [item.replace('{', '') for item in data]
        
        if self.options['sensor'] == 'MMC3630KJ':
            data = [item.replace('"MMC3630KJ Magnetometer":', '') for item in data]
        #  if self.options['job'] == 'Accelerometer':
        #      data = [item.replace('"BMI160 Accelerometer":', '') for item in data]
        if self.options['sensor'] == 'Linear Accelerator':
            data = [item.replace('"Linear Acceleration":', '') for item in data]
        
        data = [item.replace('"values"', '') for item in data]
        data = [item.replace('\n', '') for item in data]
        data = [item.replace(' ', '') for item in data]
        for i, unit in enumerate(data):
            if len(unit) != 0:
                now = datetime.datetime.now()
                self.item = []
                unit = unit.split(',')
                self.item.append(str(now))
                self.item.append(unit[0])
                self.item.append(unit[1])
                self.item.append(unit[2])
                itemWrite().write(self.item, self.options['column_list'], self.options['job'])
        avg = AverageCalc().average(data)
        print(avg)
        #  if self.options['job'] == "Accelerometer":
        #      if avg > 0.01:
                #  self.options['sensor'] = 'Linear Acceleration'
                #  self.options['job'] = "Accelerometer"
                #  self.options['duration'] = 2
                #  self.options['length'] = 60
            #      self.sensorBMI160()
            #  else:
                #  self.options['sensor'] = 'MMC3630KJ'
                #  self.options['job'] = "Magnetometer"
                #  self.options['duration'] = 2
                #  self.options['length'] = 60
                #  self.sensorBMI160()
                #  pass
        Logger("Data length: "+str(len(data)))
        Termux().sensorStop()
        Logger(self.options['job']+' '+str(datetime.datetime.now())+" Finished")

    def wifi(self):
        #  for val in self.data:
        #      self.item.append(val)
        for val in self.data.values():
            self.item.append(val)
        #  if 'center_frequency_mhz' not in self.data:
        #      self.item.append('')
        if 'center_frequency_mhz' not in self.data.keys():
            self.item.append('')
        self.item.append(str(datetime.datetime.now()))

    def gps_scan(self):
        for self.data in self.gpsscan:
            self.item.append(self.gpsscan[self.data])
        print(self.gpsscan['speed'])


    def range(self, range_type):
        if range_type == 0:
            if self.options['range_option'] is True:
                self.rangescan = rangeDetect(self.options).gps()
            else:
                self.gps_scan()
        elif range_type == 1:
            if self.options['range_option'] is True:
                self.item.append(self.rangescan)
                self.item.append(self.limit)
            else:
                self.gps_scan()

    def combo(self):
        if 'GPS' in self.options['combo']:
            if 'WifiScan' in self.options['job']:
                self.gpsscan = Termux().location()
                for self.data in self.wifiscan:
                    self.item = []
                    self.wifi()
                    range_type = 1
                    self.range(range_type)
                    self.add()

    def add(self):
        #print(self.item)
        itemWrite().write(self.item, self.options['column_list'], self.options['job'])
        #sql.add_AP(self.db_file, self.item,  self.options)

    def scan_worker(self):
        Logger('Job: '+self.options['job'])
        if 'WifiScan' in self.options['job']:
            Logger(self.options['job']+' '+"Executing")
            self.wifiscan = Termux().wifiScan()
            self.options['scan_len'] = len(self.wifiscan)
            Logger("Scan length: "+str(self.options['scan_len']))
            if self.options['isCombo']:
                self.combo()
        elif 'GPS' in self.options['job']:
            if self.options['range'] == True:
                rangeDetect(self.options).gps()
            else:
                self.gpsscan = Termux().location()
        elif 'Accelerometer' in self.options['job']:
            self.options['sensor'] = 'Linear Acceleration'
            self.sensorBMI160()
        elif 'Magnetometer' in self.options['job']:
            self.options['sensor'] = 'MMC3630KJ'
            self.sensorBMI160()
            
        elif 'Battery' in self.options['job']:
            if self.options['isLoop']:
                while True:
                    self.battery()
                    time.sleep(60)
            else:
                self.battery()
        Logger("Job finished: "+self.options['job'])
        self.options['iteration'] = str(1)
        self.options['max_iter'] = self.options['duration']
        #n = threading.Thread(target=Notify(self.options).notify())
        #n.start()

    def battery(self):
        self.item = []
        bat = Termux().Battery()
        self.item.append(str(datetime.datetime.now()))
        self.item.append(bat['current'])
        self.item.append(bat['temperature'])
        self.item.append(bat['status'])
        self.item.append(bat['percentage'])
        self.item.append(bat['plugged'])
        self.item.append(bat['health'])
        print(str(datetime.datetime.now()), "Current", bat['current'])
        self.add()

class Db():

    def __init__(self):
        self.wifikeys = [
                'date',
                'bssid',
                'frequency_mhz',
                'rssi',
                'ssid',
                'timestamp',
                'channel_bandwidth_mhz',
                'center_frequency_mhz',
                ]

        self.gpskeys = [
                'latitude',
                'longitude',
                'altitude',
                'accuracy',
                'vertical_accuracy',
                'bearing',
                'speed',
                'elapsedMs',
                'provider',
                ]

        self.batterykeys = [
            'timestamp',
            'current',
            'temperature',
            'status',
            'percentage',
            'plugged',
            'health',
                ]

        self.sensorkeys = [
                'timestamp',
                'X',
                'Y',
                'Z',
                ]


    def options(self, options):
        self.options = options
        self.keys = []
        self.db_file = self.options['db_file']
        Logger("Options init: "+self.options['job'])
        Scan().scan()
        if options['range_option'] == True:
            try:
                if len(options['limit']) != 0:
                    self.feet = options['limit'][0]
                else:
                    self.feet = options['limit']
                if self.feet == '1':
                    self.feet = 50
                self.options['limit'] = 0.305 * self.feet
                self.limit = 0.305 * self.feet
            except:
                pass
        if 'WifiScan' in options['job']:
            Logger("DB job: "+options['job'])
            self.keys = []
            if 'GPS' in options['combo']:
                if options['range_option']:
                    self.keys.append('in_range')
                    self.keys.append('range_limit')
                else:
                    for key in self.gpskeys:
                        self.keys.append(key)
                    for key in self.wifikeys:
                        self.keys.append(key)
            self.sql(options)
        
        if 'GPS' in options['job']:
            if options['range_option']:
                self.keys = ["in_range", "range_limit"]
            else:
                self.keys = self.gpskeys
            self.sql(options)
        if 'Accelerometer' or 'Magnetometer' in options['job']:
            for i in range(100):
                self.keys = self.sensorkeys
                if options['range_option']:
                    self.keys.append('in_range')
                    self.keys.append('range_limit')
                self.sql(options)
        if 'Battery' in options['job']:
            self.keys = self.batterykeys
            self.sql(options)

    def sql(self, options):
        self.options['column_list'] = ', '.join(self.keys)
        Logger("DB initiating...")
        sql.main(options)
        if options['isScan'] == True:
            self.scan()

    def scan(self):
        Termux().wake_lock()
        for self.i in range(1, int(self.options['duration'])):
            Logger("-> Scan starting "+str(self.i)+' '+self.options['job'])
            s = ThreadStart(self.options)
            s.start()
            Logger(self.options['job']+" Scan iteration: "+str(self.i)+'\n')
            self.fixed_sleep = int(self.options['length'])
            s.join()
            time.sleep(abs(self.fixed_sleep))
        Termux().wake_unlock()


class rangeDetect():
    def __init__(self, options):
        self.options = options
        self.limit = self.options['limit']
        self.range_option = options['range_option']

    def scan(self):
        for i in range(int(self.options['duration'])):
            self.gps()
            self.options['iteration'] = str(i)
            Notify(self.options).notify()
            Dates.Now().end()

    def gps(self):
        record.gpsDistance(self.options).distance(self.limit)
        if record.Range().inRange:
            self.options['inRange'] = True
        if self.range_option:
            self.option_out()
        else:
            self.option_in()
        return self.options['inRange']

    def stop(self):
        if 'Mic' in self.options['job']:
            Termux.micRecordStop()

    def start(self):
        if 'Mic' in self.options['job']:
            self.info = Termux.micInfo()
            if self.info['isRecording'] == 'False':
                Termux.micRecord()

    def option_out(self):
        if record.Range().inRange:
            self.stop()
        else:
            self.start()

    def option_in(self):
        if record.Range().inRange:
            self.start()
        else:
            self.stop()


def active(options):
    Notify(options).notify()
    Dates.Now().end()
    fixed_sleep = int(options['length']) - round(Dates.Now().result())
    time.sleep(abs(fixed_sleep))

