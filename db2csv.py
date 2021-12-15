import os
import random
import csv
from keys import Keys
from Dates import Days

class itemWrite():
    def __init__(self):
        pass

    def write(self, item, keys, instrument):
        file = '/storage/emulated/0/CSV/'+instrument+'_'+Days().today+'.csv'
        with open(file, 'a') as csvfile:
            columns = keys
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            row = {}
            try:
                for i in range(len(item)):
                    row[columns[i]] = item[i]
                writer.writerow(row)
            except:
                for i in range(len(columns)):
                    row[columns[i]] = item[i]
                writer.writerow(row)

# resolution = 0.0023956299

class AverageCalc():
    def __init__(self):
        pass


    def sample(self, average, X, Y, Z):
        sample_list = random.sample(average, 5)
        for idx, flt in enumerate(sample_list):
            if idx > 0:
                num = flt+sample_list[idx-1]
            if idx == len(sample_list) - 1:
                av = num / len(sample_list)
        Xav = X - av
        Xaverage = (X - Xav)
        Yav = Y - av
        Yaverage = (Y - Yav)
        Zav = Z - av
        Zaverage = (Z - Zav)
        
        return Xaverage, Yaverage, Zaverage

    def average(self, data):    

        res = 0.0023956299
        average = []
        av = 0

        for item in data:
            item = item[1:]
            if len(item) > 2:
                X = abs(float(item[0]))
                Y = abs(float(item[1]))
                Z = abs(float(item[2]))
            else:
                X = 0
                Y = 0
                Z = 0
            average.append(X)
        try:
            self.sample(average, X, Y, Z)
        except Exception as e:
            print(e)
            pass

