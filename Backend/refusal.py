import random
import os
import re
import numpy as np
print(os.getcwd())
from Backend.py_utils import *
from Backend import perf_calc as perf_calc

aircraft_grossweight = perf_calc.aircraft_grossweight
takeoff_factor = perf_calc.takeoff_factor
rwy_available = float(perf_calc.rwy_available)

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

def get_refusal_p1(takeoff_factor, rwy_available, data):
    xy_pair_for_rwy_avail = data[rwy_available]  #how long rwy is. Dictionary. dictionary_name[key]

    x_values = xy_pair_for_rwy_avail["y"] # x is now y
    y_values = xy_pair_for_rwy_avail["x"] # y is now x

    x_data = []
    y_data = []

    for takeoff_factor, xy_pair_for_rwy_avail in data.items():
        x_data.append(rwy_available)
        y_data.append(round(np.interp(rwy_available, x_values, y_values), 2))

    return round(np.interp(rwy_available, x_data, y_data))



    # x_values = []
    # y_values = []
    
    # for this_gross_weight, this_scales_data in data.items():

    #     x_values.append(this_gross_weight)
    #     y_values.append(round(np.interp(takeoff_factor, this_scales_data["x"], this_scales_data["y"]), 2))

    # print("refusal: ",(np.interp(rwy_available, x_values, y_values))) 
    # p1_result = round(np.interp(rwy_available, x_values, y_values))    
    # return round(np.interp(rwy_available, x_values, y_values))

##----------------------------------------------------------------------------------------------------------------------------##

# TOP_FOLDER_1 = "Backend/chart_dig/completed-takeoff/refusal-and-cef-speed"
# DIG_FILE_NAME_1 = "refusal-step-2.dig"

# data1 = {}

# chart1 = ParseDig(f'./{TOP_FOLDER_1}/dig/{DIG_FILE_NAME_1}')
# for c in  chart1.curveNames():
#     yVector1 = [row [1] for row in chart1.curve(c)]
#     xVector1 = [row [0] for row in chart1.curve(c)]
#     scale_number = float(re.sub('[^0-9]','', c.replace("-", "_")))
    
#     data1[scale_number] = {
#         "x": xVector1,
#         "y": yVector1
#     }

# def get_refusal_p2(p1_result, gwt, data1):
        
#     x_values1 = []
#     y_values1= []
    
#     for this_gross_weight, this_scales_data in data1.items():

#         x_values1.append(this_gross_weight)
#         y_values1.append(round(np.interp(aircraft_grossweight, this_scales_data["x"], this_scales_data["y"]), 2)) 

#     print("refusal2: ",(np.interp(p1_result, x_values1, y_values1)))     
#     return round(np.interp(p1_result, x_values1, y_values1))
    
