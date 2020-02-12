#!/usr/bin/python3

import os 
from datetime import date, timedelta

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
    
    if EA_or_HV == 'HV':
        # downoald Imon
        url = 'http://atlas-ddv.cern.ch:8089/multidata/getDataSafely'
        for s, e in perdelta(date(year_start, month_start - 1, day_start), date(year_stop, month_stop - 1, day_stop), timedelta(days=30)):
            cmd = 'wget --post-data "queryInfo=atlas_pvssCSC, comment_, CSC PS ' + EA_or_HV + ' ' + chamber + ' ' + layer + ' Imon, ' + s.strftime("%d-%m-%Y") + ' ' + hour_start + ':' + minute_start + ', ' + e.strftime("%d-%m-%Y") + ' ' + hour_stop + ':' + minute_stop + ', , , , , ,no, , +7!" ' + url
            os.system(cmd)

        #download Vmon
        url = 'http://atlas-ddv.cern.ch:8089/multidata/getDataSafely'
        for s, e in perdelta(date(year_start, month_start - 1, day_start), date(year_stop, month_stop - 1, day_stop), timedelta(days=30)):
            cmd = 'wget --post-data "queryInfo=atlas_pvssCSC, comment_, CSC PS ' + EA_or_HV + ' ' + chamber + ' ' + layer + ' Vmon, ' + s.strftime("%d-%m-%Y") + ' ' + hour_start + ':' + minute_start + ', ' + e.strftime("%d-%m-%Y") + ' ' + hour_stop + ':' + minute_stop + ', , , , , ,no, , +7!" ' + url
            os.system(cmd)

    if EA_or_HV == 'EA':
        # downoald Imon
        url = 'http://atlas-ddv.cern.ch:8089/multidata/getDataSafely'
        for s, e in perdelta(date(year_start, month_start - 1, day_start), date(year_stop, month_stop - 1, day_stop), timedelta(days=30)):
            cmd = 'wget --post-data "queryInfo=atlas_pvssCSC, comment_, CSC PS ' + EA_or_HV + ' ' + chamber + ' ' + layer + ' HV Imon, ' + s.strftime("%d-%m-%Y") + ' ' + hour_start + ':' + minute_start + ', ' + e.strftime("%d-%m-%Y") + ' ' + hour_stop + ':' + minute_stop + ', , , , , ,no, , +7!" ' + url
            os.system(cmd)

        #download Vmon
        url = 'http://atlas-ddv.cern.ch:8089/multidata/getDataSafely'
        for s, e in perdelta(date(year_start, month_start - 1, day_start), date(year_stop, month_stop - 1, day_stop), timedelta(days=30)):
            cmd = 'wget --post-data "queryInfo=atlas_pvssCSC, comment_, CSC PS ' + EA_or_HV + ' ' + chamber + ' ' + layer + ' HV Vmon, ' + s.strftime("%d-%m-%Y") + ' ' + hour_start + ':' + minute_start + ', ' + e.strftime("%d-%m-%Y") + ' ' + hour_stop + ':' + minute_stop + ', , , , , ,no, , +7!" ' + url
            os.system(cmd)
