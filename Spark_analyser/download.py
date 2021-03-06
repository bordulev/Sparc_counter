#!/usr/bin/python3

import os 
from datetime import date, timedelta

#Download all data needed in the analysis
def download_data(chamber, layer, year_start, month_start, day_start, hour_start, minute_start, year_stop, month_stop, day_stop, hour_stop, minute_stop):

    if (chamber == 'AL01') | (chamber == 'AL03') | (chamber == 'AL05') | (chamber == 'AL09') | (chamber == 'AL15'):
        EA_or_HV = 'EA'
    else:
        EA_or_HV = 'HV'

    def perdelta(start, end, delta):
        curr = start
        while curr < end:
            yield curr, min(curr + delta, end)
            curr += delta

    def downoload_one_peace_of_data(data_type, EA_or_HV):
        #To download current or voltage
        if EA_or_HV == 'HV':
            added_suffix = ' '
        if EA_or_HV == 'EA':
            added_suffix = ' HV '
        if (data_type == 'Imon, ') | (data_type == 'Vmon, '):
            for s, e in perdelta(date(year_start, month_start - 1, day_start), date(year_stop, month_stop - 1, day_stop), timedelta(days=30)):
                cmd = 'wget --post-data "queryInfo=atlas_pvssCSC, comment_, CSC PS ' + EA_or_HV + ' ' + chamber + ' ' + layer + added_suffix + data_type + s.strftime("%d-%m-%Y") + ' ' + hour_start + ':' + minute_start + ', ' + e.strftime("%d-%m-%Y") + ' ' + hour_stop + ':' + minute_stop + ', , , , , ,no, , +7!" ' + url
                os.system(cmd)

        #To download current or humidity
        if (data_type == 'Humidity'):
            for s, e in perdelta(date(year_start, month_start - 1, day_start), date(year_stop, month_stop - 1, day_stop), timedelta(days=30)):
                cmd = 'wget --post-data "queryInfo=atlas_pvssCSC, comment_, CSC GAS Humidifier Humidity, ' + s.strftime("%d-%m-%Y") + ' ' + hour_start + ':' + minute_start + ', ' + e.strftime("%d-%m-%Y") + ' ' + hour_stop + ':' + minute_stop + ', , , , , ,no, , +7!" ' + url
                os.system(cmd)

    url = 'http://atlas-ddv.cern.ch:8089/multidata/getDataSafely'
    # downoald Imon
    downoload_one_peace_of_data('Imon, ', EA_or_HV)
    os.rename("getDataSafely", 'getDataSafely_I') 
    # downoald Vmon
    downoload_one_peace_of_data('Vmon, ', EA_or_HV)
    os.rename("getDataSafely", 'getDataSafely_V')
    # download Humidity
    downoload_one_peace_of_data('Humidity', EA_or_HV)
    os.rename("getDataSafely", 'getDataSafely_H') 

