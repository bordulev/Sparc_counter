#!/usr/bin/python3

import datetime
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning # In order to catch warnings, when the baseline can not be fitted by exp
#from matplotlib import dates
from decimal import Decimal
import math
import warnings

def count_sparks():
    #position_Sector_layer = "AL01_L1"
    standby_current_level = 0
    current_name = "getDataSafely_I"
    voltage_name = "getDataSafely_V"
    humidity_name = "getDataSafely_H"
    time_hours_current = []
    time_hours_voltage = []
    time_hours_humidity = []

    treshold_lvl = 2 #Treshold, above which the HV for the Nominal voltage level. Default = 2
    treshold_stable_beam = 2 #Treshold, above which there is a spark.
    treshold_stable_beam_higher_long_10 = 2
    treshold_stable_beam_higher_10 = 2
    treshold_stable_beam_lower_10 = 1
    trip_level = 1.5 #how many times trip should be lower than the right boarder to be trip
    plot_length = 50
    Path_to_results = '/afs/cern.ch/user/i/ibordule/prod/Sparkcounter/output/database_txt/finalbase'
    Nominal_HV_regions_y = []
    Nominal_HV_regions_x = []
    stable_beams_y = []
    stable_beams_x = []
    year = []
    month = []
    day = []
    hour = []
    minute = []
    second = []
    msecond = []
    current = []
    linenumber = []

    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)
    
    # function, that returns the datetime parameter. Parameter == 0 for the file, that contains currents, Parameter == 1 for the file, that contains voltages
    # Parameter = 2 for the file, that contatins humidity
    def time_period(number_of_point, parameter):
        if parameter == 0:
            time = datetime.datetime(year[number_of_point], month[number_of_point], day[number_of_point],
                                     hour[number_of_point], minute[number_of_point], second[number_of_point])
        if parameter == 1:
            time = datetime.datetime(vmon_year[number_of_point], vmon_month[number_of_point], vmon_day[number_of_point],
                                     vmon_hour[number_of_point], vmon_minute[number_of_point],
                                     vmon_second[number_of_point])
        if parameter == 2:
            time = datetime.datetime(humidity_year[number_of_point], humidity_month[number_of_point], humidity_day[number_of_point],
                                     humidity_hour[number_of_point], humidity_minute[number_of_point], humidity_second[number_of_point])

        return time

    # Function, that return the text, corresponding to the date and time, when the event was registered
    # Parameter == 0 for the file, that contains currents
    # Parameter == 1 for the file, that contains voltages
    # Parameter = 2 for the file, that contatins humidity
    def time_string(number_of_point, parameter):
        if parameter == 0:
            datetime = "{0}/{1}/{2} {3}:{4}:{5}".format("%04d" % year[number_of_point], "%02d" % month[number_of_point],
                                                        "%02d" % day[number_of_point], "%02d" % hour[number_of_point],
                                                        "%02d" % minute[number_of_point], "%02d" % second[number_of_point])
        if parameter == 2:
            datetime = "{0}/{1}/{2} {3}:{4}:{5}".format("%04d" % humidity_year[number_of_point], "%02d" % humidity_month[number_of_point],
                                                        "%02d" % humidity_day[number_of_point], "%02d" % humidity_hour[number_of_point],
                                                        "%02d" % humidity_minute[number_of_point], "%02d" % humidity_second[number_of_point])
        return datetime

    def lin_func(x, a, b):
        return a * x + b

    def e_func(x, b, c, d, e):
        a = b ** (c * x + e) + d
        warnings.simplefilter("ignore", RuntimeWarning)  # Ignore the big numbers during fit
        return a

    def t_func(t, a, b, c):
        x = -b * t
        tailor = 1 + x / factorial(1) + x ** 2 / factorial(2) + x ** 3 / factorial(3) + x ** 4 / factorial(
            4) + x ** 5 / factorial(
            5)  # + x**6/factorial(6) + x**7/factorial(7) + x**8/factorial(8) + x**9/factorial(9) + x**10/factorial(10)
        return a * tailor + c

    def fit_func(x, functype, parameters):
        if functype == "lin":
            return lin_func(x, *parameters)
        if functype == "exp":
            return e_func(x, *parameters)
        if functype == "tail":
            return t_func(x, *parameters)

    # Ariphmetic mean
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

    # To change the .total_seconds() method (python 2.7) to use it in python 2.6
    def timedelta_total_seconds(timedelta):
        return (timedelta.microseconds + 0.0 + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    i = 0 # Counter
    #Extract information from file with currents
    with open(current_name) as file_currents:
        line = file_currents.read(9)
        #print(line)
        filetype = line[7:9]
        if filetype == 'HV':
            delta_char = 3
        if filetype == 'EA':
            delta_char = 0
        line = file_currents.read(18 - delta_char)
        #print(line)
        chamber = line[1:5]
        layer = line[6:8]
        line = file_currents.read(34)
        while line != "":
            if line[8] == '0': #Sometimes there is an error in the getdata file.The size of current should be 8 (not 9)
                extra_char = 1
            if line[8] == ' ':
                extra_char = 0
            #print(line)
            current.append(float(line[0:8 + extra_char]))
            day.append(int(line[9 + extra_char:11 + extra_char]))
            month.append(int(line[12 + extra_char:14 + extra_char]))
            year.append(int(line[15 + extra_char:19 + extra_char]))
            hour.append(int(line[20 + extra_char:22 + extra_char]))
            minute.append(int(line[23 + extra_char:25 + extra_char]))
            second.append(int(line[26 + extra_char:28 + extra_char]))
            msecond.append(int(line[29 + extra_char:32 + extra_char]))
            linenumber.append(i)
            i += 1
            line = file_currents.read(extra_char)
            line = file_currents.read(34)

    #Minimum time definition
    if (chamber == "AL13") & (layer == "L4"):
        min_time = 0.5
    else:
        min_time = 0.5

    #Extract information from file with voltages. The time coulumn in the Vmon is not the same, as the time column in Imon file. The voltage measurements are far more frequent
    i = 0 # Counter
    vmon_year = []
    vmon_month = []
    vmon_day = []
    vmon_hour = []
    vmon_minute = []
    vmon_second = []
    vmon_msecond = []
    voltage = []
    vmon_linenumber = []

    with open(voltage_name) as file_voltages:
        line = file_voltages.read(27 - delta_char)
        line = file_voltages.read(34) 
        while line != "":
            if line[8] == '0': #Sometimes there is an error in the getdata file.The size of current should be 8 (not 9)
                extra_char = 1
            if line[8] == ' ':
                extra_char = 0
            voltage.append(float(line[0:8 + extra_char]))
            vmon_day.append(int(line[9 + extra_char:11 + extra_char]))
            vmon_month.append(int(line[12 + extra_char:14 + extra_char]))
            vmon_year.append(int(line[15 + extra_char:19 + extra_char]))
            vmon_hour.append(int(line[20 + extra_char:22 + extra_char]))
            vmon_minute.append(int(line[23 + extra_char:25 + extra_char]))
            vmon_second.append(int(line[26 + extra_char:28 + extra_char]))
            vmon_msecond.append(int(line[29 + extra_char:32 + extra_char]))
            vmon_linenumber.append(i)
            i += 1
            line  = file_voltages.read(extra_char)
            line = file_voltages.read(34)
            
    humidity_value = []
    humidity_year = []
    humidity_month = []
    humidity_day = []
    humidity_hour = []
    humidity_minute = []
    humidity_second = []
    humidity_msecond = []
    humidity_timestamp = [] #in epoch

    with open(humidity_name) as file_humidity:
        #Read header
        line = file_humidity.read(29)
        #Read the rest of the file
        line = file_humidity.read()
        humidity_all_data = line.split(", ")
        for humidity_one_vector_of_data in humidity_all_data:
            humidity_one_vector_of_data_list = humidity_one_vector_of_data.split(" ")
            humidity_value.append(float(humidity_one_vector_of_data_list[0]))
            humidity_day.append(int(humidity_one_vector_of_data_list[1][0:2]))
            humidity_month.append(int(humidity_one_vector_of_data_list[1][3:5]))
            humidity_year.append(int(humidity_one_vector_of_data_list[1][6:10]))
            humidity_hour.append(int(humidity_one_vector_of_data_list[2][0:2]))
            humidity_minute.append(int(humidity_one_vector_of_data_list[2][3:5]))
            humidity_second.append(int(humidity_one_vector_of_data_list[2][6:8]))
            humidity_msecond.append(int(humidity_one_vector_of_data_list[2][9:12]))

    #Fill the list with the timestamps (in epoch time) for Humidity values
    for i in range(0, len(humidity_value)):
        humidity_timestamp.append(time_period(i, 2))

    
    #calculating the time scale (x-axes should be in hours) for currents
    for i in range(0, len(current)):
        timedelta = time_period(i, 0) - time_period(0, 0)
        seconds = timedelta_total_seconds(timedelta)
        hours = seconds / 3600
        time_hours_current.append(hours)

    #calculating the time scale (x-axes should be in hours) for voltages
    for i in range(0, len(voltage)):
        timedelta = time_period(i, 1) - time_period(0, 0)
        seconds = timedelta_total_seconds(timedelta)
        hours = seconds / 3600
        time_hours_voltage.append(hours)

    #Find the Standby period, where the voltage is less than 1300
    standby_periods = []
    HV_values_ready = []
    HV_times_ready = []
    start_point = 0
    stop_point = 0
    start_limit_founded = 0
    stop_limit_founded = 0
    HV_ready_foundflag = 0
    for i in range (0, len(voltage)-1):
        standby_period = []
        if (voltage[i] > 1310) and (voltage [i+1] <= 1310):
            start_point = time_hours_voltage [i+1]
            start_limit_founded = 1
        # This is needed not to count the HV trip
        if (voltage[i] < 1000):
            start_limit_founded = 0
        if (((voltage[i] <= 1310) and (voltage[i+1] > 1310))or(i == len(voltage) - 2)) and (start_limit_founded == 1):
            stop_point = time_hours_voltage [i]
            stop_limit_founded = 1
        if (start_limit_founded == 1) and (stop_limit_founded == 1):
            standby_period = [start_point, stop_point]
            standby_periods = standby_periods + [standby_period]
            start_limit_founded = 0
            stop_limit_founded = 0
        # Find the level of HV when the state is ready
        if HV_ready_foundflag == 0:
            if voltage[i] > 1400:
                if voltage[i] > voltage[i+1]:
                    HV_values_ready.append(voltage[i])
                    HV_times_ready.append(time_period(i,1))
                    HV_ready_foundflag = 1
        if voltage[i] < 1400:
            HV_ready_foundflag = 0
#    print (len(HV_values_ready))

    #If the average HV is lower than the certain level, the treshold for the stable beam should also be lower
    if len (HV_values_ready) != 0:
        avg_HV = sum(HV_values_ready) / len (HV_values_ready)
    else:
        avg_HV = 0
    if avg_HV < 1700:
        treshold = treshold_lvl / 2
    else:
        treshold = treshold_lvl

    #Find the level of a current, corresponding to the standby mode
    standby_current_number = 0
    standby_current_sum = 0
    if standby_current_level == 0: #if not defined by user
        for i in range (0, len(standby_periods)):        #Look in all standby periods
            for j in range (0, len(time_hours_current)):             #Search in all the times, when the current is recorded
                if (time_hours_current[j] > standby_periods[i][0]) and (time_hours_current[j] < standby_periods[i][1]):   #If the time, when current was recorded lies in a range where there is a standby period (according to voltage)
                    standby_current_number += 1
                    standby_current_sum += current[j]
        if (standby_current_number < len(standby_periods)) or (standby_current_number == 0): # If on each region of Standby there is less than one point with current
            standby_current_level = 0.7
        else:
            standby_current_level = standby_current_sum / standby_current_number #arithmetic average for all standby current

    # If the the stand by current is equal to 0 it is not the real physical situation and the treshold should be increased
    if standby_current_level < 0.1:
        treshold = treshold + treshold*1/3

    #print standby_current_level

    #standby_current_level = 0.3
    treshold_Nominal_HV = standby_current_level + treshold

    #Search for regions above treshold
    region_x = []
    region_y = []
    for i in range(0, len(current)):
        if current[i] >= treshold_Nominal_HV:
            region_y.append(current[i])      # Create the list of currents above treshold
            region_x.append(i)               # Create the number of dots above the treshold
            if i < (len(current) - 1):              # The process of separation of all area above the treshold on several parts, where the current is above the treshold
                if (current [i+1] < treshold_Nominal_HV) or (i+1 == len(current) - 1):
                    if len(region_y) > 4:           # The minimal length of Nominal NV region should be achieved
                        Nominal_HV_regions_y.append(region_y)    #Each element of this list is a number of currents in a certain region above the treshold
                        Nominal_HV_regions_x.append(region_x)    #Each element of this list is a number of numbers in a certain region above the treshold
                    region_x = []
                    region_y = []

    #Lets find the values of average current above treshold for each region
    listof_avgvalues = []
    for j in range(0, len(Nominal_HV_regions_y)):            # Search in all region above the treshold
        startpoint = int(round(len(Nominal_HV_regions_y[j])/3))
        stoppoint = int(round(2*len(Nominal_HV_regions_y[j])/3))
        listwithouttrips = Nominal_HV_regions_y[j][startpoint:stoppoint]
        avgvalue = sum(listwithouttrips)/len(listwithouttrips)
        listof_avgvalues.append(avgvalue)

    #Correct the region above treshold. Almost the same procedure that the "Search for regions above treshold" but with the new condition
    Correct_Nominal_HV_regions_y = []
    Correct_Nominal_HV_regions_x = []
    region_x = []
    region_y = []
    for j in range(0, len(Nominal_HV_regions_y)):
        xmini = time_hours_current[Nominal_HV_regions_x[j][1]]/plot_length
        xmaxi = time_hours_current[Nominal_HV_regions_x[j][len(Nominal_HV_regions_x[j]) - 1]]/plot_length
        region_length = (xmaxi - xmini)*plot_length
        if listof_avgvalues[j] < 4:
            trip_level = 1.5
        else:
            if region_length < 8:
                trip_level = 1.6
            elif region_length > 19:
                trip_level = 4
            else:
                trip_level = 2.5
        for i in range(0, len(Nominal_HV_regions_y[j])):
            if Nominal_HV_regions_y[j][i] >= listof_avgvalues[j]/trip_level:    #New condition. All the points should be higher than the 1/3d of the first maximum point of Nominal_HV_region
                region_y.append(Nominal_HV_regions_y[j][i])
                region_x.append(Nominal_HV_regions_x[j][i])
                if i < (len(Nominal_HV_regions_y[j]) - 1):
                    if (Nominal_HV_regions_y[j][i+1] < listof_avgvalues[j]/trip_level) or (i+1 == len(Nominal_HV_regions_y[j]) - 1): #New condition. If the point is lower than the 1/3d of the first maximum point of Nominal_HV_region, it doesn't go there, and the search of next NominalHV region starts
                        if len(region_y) > 4:
                            Correct_Nominal_HV_regions_y.append(region_y)
                            Correct_Nominal_HV_regions_x.append(region_x)
                        region_x = []
                        region_y = []
                if i == len(Nominal_HV_regions_y[j]) - 1:
                    region_x = []
                    region_y = []

    #Search for the stable beam interval (the begin and the end of it)
    left_boarder_founded = 0
    right_boarder_founded = 0
    for j in range(0, len(Correct_Nominal_HV_regions_y)):            # Search in all region above the treshold
        region_x = []
        region_y = []
        if len(Correct_Nominal_HV_regions_y[j]) > 6:
            for i in range(0, len(Correct_Nominal_HV_regions_y[j]) - 1):     # Search in a certain region for start of the stable beam region
                if  (Correct_Nominal_HV_regions_y[j][i] >  Correct_Nominal_HV_regions_y[j][i+1]) and (i != 0):
                    region_y.append(Correct_Nominal_HV_regions_y[j][i])
                    region_x.append(Correct_Nominal_HV_regions_x[j][i])
                    left_boarder_founded = 1
                    break                               # Stop to search, when it is founded
            if left_boarder_founded == 1:
                for i in range(len(Correct_Nominal_HV_regions_y[j]) - 1, 0, -1): # Search in a certain region for stop of the stable beam region
                    if  Correct_Nominal_HV_regions_y[j][i] >  Correct_Nominal_HV_regions_y[j][i-1]:
                        if (Correct_Nominal_HV_regions_y[j][i]) - (Correct_Nominal_HV_regions_y[j][i-1]) < treshold_stable_beam:  #to prevent the end of fpeff to be at the spark peak
                            region_y.append(Correct_Nominal_HV_regions_y[j][i])
                            region_x.append(Correct_Nominal_HV_regions_x[j][i])
                            right_boarder_founded = 1
                        else:
                            region_y.append(Correct_Nominal_HV_regions_y[j][i-1])
                            region_x.append(Correct_Nominal_HV_regions_x[j][i-1])
                            right_boarder_founded = 1
                        if right_boarder_founded == 1:
                            break                               # Stop to search, when it is founded
            if (left_boarder_founded == 1) and (right_boarder_founded == 1):
                if region_x[0] < region_x[1]:                 # Condition for the stable beam region. It should contatin more than one point. In other case the start point will be after the stop point or they will be equal
                    region_y = [j] + region_y               # Every region of stable beam is characterised by the [number of the region above the treshold, stable beam start point, stable beam stop point]. If there is no stable beam region in the region above treshold, it is not included in the final list
                    region_x = [j] + region_x
                    stable_beams_y.append(region_y)
                    stable_beams_x.append(region_x)
                region_x = []
                region_y = []
                left_boarder_founded = 0
                right_boarder_founded = 0

    #Correct the HV_values_ready. The number of them should be equal not the the number of HV_Nominal regions, but the number of Correct_HV_Nominal regions
    Correct_HV_values_ready = []
    for i in range(0, len(stable_beams_x)):
        k = 0
        for j in range(0, len(HV_times_ready)):
            diff = timedelta_total_seconds(time_period(stable_beams_x[i][1], 0) - HV_times_ready[j])
            if diff > 0:
                k += 1
        if len(HV_values_ready) != 0: #If there are some stable beams
            Correct_HV_values_ready.append(HV_values_ready[k-1])
    #print (len(Correct_HV_values_ready))
    if len(Correct_HV_values_ready) != 0:
        #Search for the sparks
        print("Chamber          layer         timestamp                  Amp              Baseline          Timediff           HV")
        list_of_datetimes = [] # for the dynamics graph
        period_rate_local = []
        sparks_sector = []
        sparks_layer = []
        sparks_amplitudes = []
        sparks_amplitudes_hist = []
        sparks_time_differences = []   #time difference between two neighbour sparks, or (in case of the first spark) - between the spark and the begin of the stable beam
        sparks_time_differences_hist = []
        sparks_timestamp = [] #When the spark occured
        sparks_baseline_current = []
        sparks_HV = []
        sparks_humidity_value = []
        sparks_humidity_timestamp = []  #in nice format
        menStd = [] #the list for error bars for sparks rate

        #print (stable_beams_x[0])
        for j in range(0, len(stable_beams_x)):                     # Look in every region of stable beams
            count_local = 0      #sparks counter
            x1 = time_hours_current[stable_beams_x[j][1]]                   #to calculate the linear dependence
            y1 = stable_beams_y[j][1]                   #to calculate the linear dependence
            x2 = time_hours_current[stable_beams_x[j][2]]                   #to calculate the linear dependence
            y2 = stable_beams_y[j][2]                   #to calculate the linear dependence
            time_previos_peak = x1
            if (x2 - x1) > min_time:  #the length of stable beams should be longer than the minimum length, defined by user
                x_for_fit = time_hours_current[stable_beams_x[j][1]:stable_beams_x[j][2]]
                y_for_fit = current[stable_beams_x[j][1]:stable_beams_x[j][2]]
                # Least squares fit
                #print (len(x_for_fit))
                if len(x_for_fit) < 5: #In order to fit by polinom, the number of points(fitting) shouls be more than the number of constants
                    print('to low number of points for fit')
                    continue
                func_type = "exp"
                if y_for_fit[0] >= 12:               # If the first current in stable beam is low, the treshold for spark should be low
                    initial_params = [1.0, -0.09, -850, 495]
                else:
                    initial_params = [1, 1, 1, 1]
                try:                                 # Sometimes the exp fit still does not work. In this case, the error is raised and the linear fit start
                    warnings.simplefilter("error", OptimizeWarning)
                    #print (x_for_fit)
                    #print (y_for_fit)
                    Params, pcov = curve_fit(e_func, x_for_fit, y_for_fit, maxfev = 1000000, p0=initial_params)
                    if Params[1]>0:         # In the case of it > 2 the exp fit represents horizontal line
                        print ("Params[1]>0")
                        Params, pcov = curve_fit(lin_func, x_for_fit, y_for_fit)
                        func_type = "lin"
                        # When the fit output is the increasing line. It is better to make it parralel to OX line
                        if Params[0]>0:
                            Params[0] = 0
                            Params[1] = mean(y_for_fit)
                except OptimizeWarning:
                    print ("The exponent fit failed")
                    Params, pcov = curve_fit(lin_func, x_for_fit, y_for_fit)
                    if Params[0]>0:
                            Params[0] = 0
                            Params[1] = mean(y_for_fit)
                    func_type = "lin"
                except ValueError:
                    print ("value error")
                    Params, pcov = curve_fit(lin_func, x_for_fit, y_for_fit)
                    if Params[0]>0:
                            Params[0] = 0
                            Params[1] = mean(y_for_fit)
                    func_type = "lin"
                except RuntimeError:
                    print ("Runtime error: Could not fit by exponent")
                    Params, pcov = curve_fit(lin_func, x_for_fit, y_for_fit)
                    if Params[0]>0:
                            Params[0] = 0
                            Params[1] = mean(y_for_fit)
                    func_type = "lin"
                #print (Params)
                region_x = linenumber[stable_beams_x[j][1]:(stable_beams_x[j][2] + 4)] # Three points longer than the stable beam in case the peak in the end
                region_y = current[stable_beams_x[j][1]:(stable_beams_x[j][2] + 4)]# Three points longer than the stable beam in case the peak in the end
                long_period = 0
                if region_y[0] >= 10:               # If the first current in stable beam is low, the treshold for spark should be low
                    treshold_stable_beam = treshold_stable_beam_higher_10
                    if (x2 - x1) >= 5:              # On longer beriods - the baseline oscillations are lower, and the treshold could be also lower.
                        long_period = 1
                else:
                    treshold_stable_beam = treshold_stable_beam_lower_10

                #print (treshold_stable_beam, "     ", long_period)
                for i in range(0, len(region_y)):
                    # The treshold for long stable beam period is implemented only for 2nd and 3rd parts (of 4 parts) of the stable beam
                    if (i > len(region_y) / 4) and (i < 3 * len(region_y) / 4) and (long_period == 1):
                        treshold_stable_beam = treshold_stable_beam_higher_long_10
                    x = time_hours_current[region_x[i]]
                    y = region_y[i]
                    if y > (treshold_stable_beam + fit_func(x, func_type, Params)): #If there is a spark
                        if (x > time_hours_current[stable_beams_x[j][1]]):                                                       # Not to count the first spark of the stable beam region
                            if i+1 < len(region_y):
                                if region_y[i+1] < (treshold_stable_beam + fit_func(x, func_type, Params)):                                # Count only one yellow dot on a spark's peak
                                    # Calculate the amplitude of the spark and the distance between two peaks
                                    if i-1 != stable_beams_x[j][1] - 1:                                                         # Not to count the first spark of the stable beam region
                                        spark_current_peak = max([region_y[i], region_y[i-1]])
                                    else:
                                        spark_current_peak = region_y[i]
                                    if spark_current_peak == region_y[i]:
                                        time_new_peak = time_hours_current[region_x[i]]
                                        spark_baseline = fit_func(time_new_peak, func_type, Params)
                                    if spark_current_peak == region_y[i - 1]:
                                        time_new_peak = time_hours_current[region_x[i - 1]]
                                        spark_baseline = fit_func(time_new_peak, func_type, Params)

                                    delta_time = (time_new_peak - time_previos_peak)*3600 #seconds
                                    if delta_time != 0:     # Sometimes to one sparks corresponds two inputs in database. This condition is needed to force it
                                        Amp = spark_current_peak - spark_baseline
                                        sparks_amplitudes.append(Amp)
                                        sparks_amplitudes_hist.append(Amp)
                                        sparks_baseline_current.append(spark_baseline)
                                        sparks_time_differences.append(delta_time)
                                        sparks_time_differences_hist.append(delta_time)
                                        sparks_timestamp.append(time_string(region_x[i], 0))
                                        #Define the time and the value of Humidity, corresponding to the spark
                                        #Find the point in humidity data, that is closest by time to the one time of the spark
                                        humid_closest_point_num = min(range(len(humidity_timestamp)), key=lambda humid_point_num: abs(humidity_timestamp[humid_point_num]-time_period(region_x[i], 0)))
                                        #Fill the closest value and time of hyumidity to the corresponding lists
                                        sparks_humidity_timestamp.append(time_string(humid_closest_point_num, 2))
                                        sparks_humidity_value.append(humidity_value[humid_closest_point_num])
                                        sparks_sector.append(chamber)
                                        #print (len(sparks_amplitudes))
                                        sparks_layer.append(layer)
                                        sparks_HV.append(Correct_HV_values_ready[j])
                                        time_previos_peak = time_new_peak
                                        count_local += 1
                                        first_spark_founded = 0
                                        # Print the data for the user: Chamber layer timestamp Amp Baseline Timediff HV Humidity_value_Humidity_timestamp
                                        print_str_to_terminal = str(chamber)+"             "+str(layer)+"            "+str(time_string(region_x[i], 0))+"        "+("%.2f" % Amp)+"             "+("%.2f" % spark_baseline)+"             "+("%.1f" % delta_time)+"             "+str(Correct_HV_values_ready[j])
                                        print (print_str_to_terminal)
                    #This condition is needed to make an entry at the end of the run (AMP = -1)
                    elif i == len(region_y) - 1:
                        delta_time = (time_hours_current[region_x[i]] - time_previos_peak)*3600 #seconds
                        sparks_sector.append(chamber)
                        sparks_layer.append(layer)
                        sparks_timestamp.append(time_string(region_x[i], 0))
                        sparks_amplitudes.append(-1)
                        #Define the time and the value of Humidity, corresponding to the spark
                        humid_closest_point_num = min(range(len(humidity_timestamp)), key=lambda humid_point_num: abs(humidity_timestamp[humid_point_num]-time_period(region_x[i], 0)))
                        sparks_humidity_timestamp.append(time_string(humid_closest_point_num, 2))
                        sparks_humidity_value.append(humidity_value[humid_closest_point_num])
                        sparks_baseline_current.append(fit_func(time_hours_current[region_x[i]], func_type, Params))
                        sparks_time_differences.append(delta_time)
                        if len(Correct_HV_values_ready) != 0: #If there are no stable beams at this period of time. There will be no data in Correct_HV_values_ready list
                            sparks_HV.append(Correct_HV_values_ready[j])



                rate_local = count_local / (x2 - x1) #in hours
                rate_local = round(rate_local,2) # round it by two digits after decimal point
                period_rate_local.append(rate_local)
                list_of_datetimes.append(time_period(stable_beams_x[j][2], 0))
    
    if len(Correct_HV_values_ready) != 0:
    #Open file to write the results in it
        filename = Path_to_results + ".txt"
        file = open(filename,"a+")
        for i in range(0, len(sparks_amplitudes)):
            print_str = str(sparks_sector[i])+"             "+str(sparks_layer[i])+"            "+str(sparks_timestamp[i])+"        "+("%.2f" % sparks_amplitudes[i])+"             "+("%.2f" % sparks_baseline_current[i])+"             "+("%.1f" % sparks_time_differences[i])+"             " + str(sparks_HV[i]) + "             " + str(sparks_humidity_value[i]) 
            file.write(print_str)
            file.write("\n")
        file.close()
    return 1
