#!/usr/bin/python3

import spark_counter_181031
import download
import os

hour_start = '00'
minute_start = '00'

hour_stop = '00'
minute_stop = '00'

year = 2018

#list_of_chambers = ['AL01', 'AL03', 'AL05', 'AL07', 'AL09', 'AL11', 'AL13', 'AL15', 'AS02', 'AS04', 'AS06', 'AS08', 'AS10', 'AS12', 'AS14', 'AS16', 'CL01', 'CL03', 'CL05', 'CL07', 'CL09', 'CL11', 'CL13', 'CL15', 'CS02', 'CS04', 'CS06', 'CS08', 'CS10', 'CS12', 'CS14', 'CS16']
#list_of_layers = ['L1', 'L2', 'L3', 'L4']

#list_of_chambers = ['AL01']
#list_of_layers = ['L1']

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

#days_start = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

#print (month)
day_start = day_stop - 1
if ((month == 8) | (month == 9) | (month == 11)) and (day_stop == 1):
    day_start = 31
if ((month == 10) | (month == 12)) and (day_stop == 1):
    day_start = 30

#if (month == 9) and (day_start == 28):
#    day_stop = 30
print("Month: ", month, "Day start: ", day_start, " time start: ", hour_start, ":", minute_start, "Day stop: ", day_stop, " time stop: ", hour_stop, ":", minute_stop)
print("Processing")
print(chamber, layer)
download.download_data(chamber, layer, year, month + 1, day_start, hour_start, minute_start, year, month + 1, day_stop, hour_stop, minute_stop)
statinfo_I = os.stat('getDataSafely')
statinfo_V = os.stat('getDataSafely.1')
print("The size of current file is: ", statinfo_I.st_size)
print("The size of voltage file is: ", statinfo_V.st_size)
if (statinfo_I.st_size < 280) | (statinfo_V.st_size < 280):
    os.remove("getDataSafely")
    os.remove("getDataSafely.1")
    #os.rename("getDataSafely", 'getDataSafely' + str(i))
    #os.rename("getDataSafely.1", 'getDataSafely.1' + str(i))
    print("No data. Files removed")
else:
    #(chamber, layer, year_start, month_start, day_start, hour_start, minute_start, year_stop, month_stop, day_stop, hour_stop, minute_stop)
    spark_counter_181031.count_sparks()
    #os.rename("getDataSafely", 'getDataSafely' + str(i))
    #os.rename("getDataSafely.1", 'getDataSafely.1' + str(i))
    os.remove("getDataSafely")
    os.remove("getDataSafely.1")
    print("Files removed")
