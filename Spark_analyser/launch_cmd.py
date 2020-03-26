#!/usr/bin/python3

import spark_counter_181031
import download
import os

hour_start = '00'
minute_start = '00'

hour_stop = '00'
minute_stop = '00'

year = 2018

print("launched")

file_with_chambers = open("cfg_chamber", "r")
line = file_with_chambers.read(4)
chamber = line
file_with_chambers.close()

file_with_layers = open("cfg_layer", "r")
line = file_with_layers.read(2)
layer = line
file_with_layers.close()

file_with_months = open("cfg_month", "r")
line = file_with_months.read(2)
month = int(line)
file_with_months.close()

file_with_days_stop = open("cfg_day_stop", "r")
line = file_with_days_stop.read(2)
day_stop = int(line)
file_with_days_stop.close()

day_start = day_stop - 1
if ((month == 8) | (month == 9) | (month == 11)) and (day_stop == 1):
    day_start = 31
if ((month == 10) | (month == 12)) and (day_stop == 1):
    day_start = 30

print("Month: ", month, "Day start: ", day_start, " time start: ", hour_start, ":", minute_start, "Day stop: ", day_stop, " time stop: ", hour_stop, ":", minute_stop)
print("Processing")
print(chamber, layer)
download.download_data(chamber, layer, year, month + 1, day_start, hour_start, minute_start, year, month + 1, day_stop, hour_stop, minute_stop)
statinfo_I = os.stat('getDataSafely_I')
statinfo_V = os.stat('getDataSafely_V')

print("The size of current file is: ", statinfo_I.st_size)
print("The size of voltage file is: ", statinfo_V.st_size)
if (statinfo_I.st_size < 280) | (statinfo_V.st_size < 280):
    os.remove("getDataSafely_I")
    os.remove("getDataSafely_V")
    os.remove("getDataSafely_H")
    print("No data. Files removed")
else:
    spark_counter_181031.count_sparks()
    os.remove("getDataSafely_I")
    os.remove("getDataSafely_V")
    os.remove("getDataSafely_H")
    print("Files removed")
