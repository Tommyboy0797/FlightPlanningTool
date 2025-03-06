import random
import os
import re
import numpy as np
from pprint import pprint
print(os.getcwd())
from Backend.py_utils import *
from Backend import perf_calc as perf_calc

uncorr_ref_spd = 140
rwy_slope = 2

def get_refusal_p1(takeoff_factor, rwy_available): 
    
    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-step-1.dig" 

    data = {}

    chart = ParseDig(f'./{TOP_FOLDER}/dig/{DIG_FILE_NAME}')
    for c in  chart.curveNames():
        yVector = [row [1] for row in chart.curve(c)]
        xVector = [row [0] for row in chart.curve(c)]
        scale_number = float(re.sub('[^0-9]','', c.replace("-", "_")))
        
        data[scale_number] = {
            "x": xVector,
            "y": yVector
        }

    runway_scale_set = [] # runway scale (2,3,4, -> 14)
    result_basedon_to_factor_and_rwylen = [] # result for given takeoff factor scale based on runway length  

    for rwy_scale, xy_pair_for_rwy_avail in data.items():
        xy_pair_for_rwy_avail = data[rwy_scale]  #how long rwy is. Dictionary. dictionary_name[key] Key here is rwy_scale which is 2.0, 3.0, 4.0 etc

        x_values = xy_pair_for_rwy_avail["y"] # x is now y
        y_values = xy_pair_for_rwy_avail["x"] # y is now x

        runway_scale_set.append(rwy_scale)
        result_basedon_to_factor_and_rwylen.append(round(np.interp(takeoff_factor, x_values, y_values), 2))

    resultp1 = np.interp(rwy_available, runway_scale_set, result_basedon_to_factor_and_rwylen)

    return resultp1



def get_refusal_p2(result, aircraft_grossweight): 
    
    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-step-2.dig"

    data = {}

    chart = ParseDig(f'./{TOP_FOLDER}/dig/{DIG_FILE_NAME}')
    for c in  chart.curveNames():
        yVector = [row [1] for row in chart.curve(c)]
        xVector = [row [0] for row in chart.curve(c)]
        scale_number = float(re.sub('[^0-9]','', c.replace("-", "_")))
        
        data[scale_number] = {
            "x": xVector,
            "y": yVector
        }

    runway_scale_set = [] 
    result_basedon_to_factor_and_rwylen = []   

    for rwy_scale, xy_pair_for_rwy_avail in data.items():
        xy_pair_for_rwy_avail = data[rwy_scale]  

        x_values = xy_pair_for_rwy_avail["x"] 
        y_values = xy_pair_for_rwy_avail["y"] 

        runway_scale_set.append(rwy_scale)
        result_basedon_to_factor_and_rwylen.append(round(np.interp(result, x_values, y_values), 2))
        
    result = np.interp(aircraft_grossweight, runway_scale_set, result_basedon_to_factor_and_rwylen)

    return round(result)




def get_refusal_p3(uncorrected_ref_speed, rwy_slope): #runway slope

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-runway-slope.dig"

    data = {}

    chart = ParseDig(f'./{TOP_FOLDER}/dig/{DIG_FILE_NAME}')
    for c in  chart.curveNames():
        yVector = [row [1] for row in chart.curve(c)]
        xVector = [row [0] for row in chart.curve(c)]
        scale_number = float(re.sub('[^0-9]','', c.replace("-", "_")))
        
        data[scale_number] = {
            "x": xVector,
            "y": yVector
        }
    
    runway_slope_scale = []
    result_slope = []

    for slope_scale, xy_pair_slope in data.items():
        xy_pair_slope = data[slope_scale]

        x_values = xy_pair_slope["x"]
        y_values = xy_pair_slope["y"]

        runway_slope_scale.append(slope_scale)
        result_slope.append(np.interp(rwy_slope,x_values, y_values))

    result = np.interp(uncorrected_ref_speed, runway_slope_scale, result_slope)

    return round(result)

def get_refusal_p4(prev_data, wind_speed, tail_or_head):

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-runway-slope.dig"

    data = {}

    chart = ParseDig(f'./{TOP_FOLDER}/dig/{DIG_FILE_NAME}')
    for c in  chart.curveNames():
        yVector = [row [1] for row in chart.curve(c)]
        xVector = [row [0] for row in chart.curve(c)]
        scale_number = float(re.sub('[^0-9]','', c.replace("-", "_")))
        
        data[scale_number] = {
            "x": xVector,
            "y": yVector
        }

    if tail_or_head == "Headwind":
        wind_speed = wind_speed * 0.5 # apply a +50% factor to reported headwind
    elif tail_or_head == "Tailwind":
        wind_speed = wind_speed * 1.5 # apply a +150% factor to reported headwind
    else:
        wind_speed = wind_speed # do nothing if its a crosswind

    runway_windscale = []
    result_wind = []

    for windscale, xy_pair_wind in data.items():
        xy_pair_wind = data[windscale]

        x_values = xy_pair_wind["x"]
        y_values = xy_pair_wind["y"]

        runway_windscale.append(windscale)
        result_wind.append(np.interp(wind_speed, x_values, y_values))
    
    result = np.interp(prev_data, runway_windscale, result_wind)

    return round(result)