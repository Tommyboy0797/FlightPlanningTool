import random
import os
import re
import numpy as np
from pprint import pprint
print(os.getcwd())
from Backend.py_utils import *
from Backend import perf_calc as perf_calc

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
    DIG_FILE_NAME = "wind-velocity-for-refusal.dig"

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

    wind_speed = int(wind_speed)

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

def get_refusal_p5(prev_data, dragindex):

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-drag-index.dig"

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
    drag_index_scale = []
    result_drag = []

    for dragscale, xy_pair_drag in data.items():
        xy_pair_drag = data[dragscale]

        x_values = xy_pair_drag["x"]
        y_values = xy_pair_drag["y"]

        drag_index_scale.append(dragscale)
        result_drag.append(np.interp(dragindex, x_values, y_values))

    result = np.interp(prev_data, drag_index_scale, result_drag)

    return round(result)

def get_refusal_p6(prev_data, rcr):

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-rcr.dig"

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
    
    rcr_scale = []
    result_rcr = []

    for rcrscale, xy_pair_rcr in data.items():
        xy_pair_rcr = data[rcrscale]

        x_values = xy_pair_rcr["x"][::-1]
        y_values = xy_pair_rcr["y"][::-1]

        rcr_scale.append(rcrscale)
        result_rcr.append(np.interp(rcr, x_values, y_values))

    result = np.interp(prev_data, rcr_scale, result_rcr)

    return round(result)

def get_refusal_p7(prev_data, rsc):

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-rsc.dig"

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

    rsc_scale = []
    result_rsc = []

    for rscscale, xy_pair_rsc in data.items():
        xy_pair_rsc = data[rscscale]

        x_values = xy_pair_rsc["x"]
        y_values = xy_pair_rsc["y"]

        rsc_scale.append(rscscale)
        result_rsc.append(np.interp(rsc, x_values, y_values))

    result = np.interp(prev_data, rsc_scale, result_rsc)
    return round(result)

def get_refusal_p8(prev_data, yes_no):

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "atcs-for-refusal.dig"

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

    if yes_no == True or yes_no == "true": # if the atcs is operational
        yes_no = 0
    elif yes_no == False or yes_no == "false": # if the atcs is not operational
        yes_no = 1
    else: yes_no = 0


    atcs_scale = []
    result_atcs = []

    for atcscale, xy_pair_atcs in data.items():
        xy_pair_atcs = data[atcscale]

        x_values = xy_pair_atcs["x"]
        y_values = xy_pair_atcs["y"]

        atcs_scale.append(atcscale)
        result_atcs.append(np.interp(yes_no, x_values, y_values))

    result = np.interp(prev_data,atcs_scale,result_atcs)

    return round(result)


def get_refusal_p9(prev_data, yes_no):  

    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
    DIG_FILE_NAME = "refusal-anti-skid.dig"

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

    if yes_no == True or yes_no == "true": # if the AS is operational
        yes_no = 0
    elif yes_no == False or yes_no == "false": # if the AS is not operational
        yes_no = 1
    else: yes_no = 0


    as_scale = []
    result_as = []

    for asscale, xy_pair_as in data.items():
        xy_pair_as = data[asscale]

        x_values = xy_pair_as["x"]
        y_values = xy_pair_as["y"]

        as_scale.append(asscale)
        result_as.append(np.interp(yes_no, x_values, y_values))

    result = np.interp(prev_data,as_scale,result_as)

    return round(result) # fully corrected refusal IAS!
