import random
import os
import re
import numpy as np
from pprint import pprint
print(os.getcwd())
from Backend.py_utils import *
from Backend import perf_calc as perf_calc

# the data this requires: grossweight, altitude, temperature deviation




def get_uncorrected_ff_endurance(gwt, pressure_alt):

    TOP_FOLDER = "Backend/chart_dig/completed-cruise/max-endurance-fuel-flow-4-eng"
    DIG_FILE_NAME = "uncorrected.dig"

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

    gwt_scale_set = []
    result_gwt = []

    for gwt_scale, xy_pair_gwt in data.items():
        xy_pair_gwt = data[gwt_scale]

        x_values = xy_pair_gwt["x"]
        y_values = xy_pair_gwt["y"]

        gwt_scale_set.append(gwt_scale)
        result_gwt.append(np.interp(pressure_alt,x_values,y_values))
    
    result = np.interp(gwt,gwt_scale_set,result_gwt)

    return result


def get_corrected_ff_endurancep1(prev_data, temp_dev):

    TOP_FOLDER = "Backend/chart_dig/completed-cruise/max-endurance-fuel-flow-4-eng"
    DIG_FILE_NAME = "corrected-temp.dig"

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

    prev_scale_set = []
    result_prev = []

    for gwt_scale, xy_pair_gwt in data.items():
        xy_pair_gwt = data[gwt_scale]

        x_values = xy_pair_gwt["x"]
        y_values = xy_pair_gwt["y"]

        prev_scale_set.append(gwt_scale)
        result_prev.append(np.interp(temp_dev,x_values,y_values))
    
    result = np.interp(prev_data,prev_scale_set,result_prev)

    return result

def get_corrected_ff_endurancep2(prev_data, drag):

    TOP_FOLDER = "Backend/chart_dig/completed-cruise/max-endurance-fuel-flow-4-eng"
    DIG_FILE_NAME = "corrected-drag.dig"

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

    prev_scale_set = []
    result_prev = []

    for gwt_scale, xy_pair_gwt in data.items():
        xy_pair_gwt = data[gwt_scale]

        x_values = xy_pair_gwt["x"]
        y_values = xy_pair_gwt["y"]

        prev_scale_set.append(gwt_scale)
        result_prev.append(np.interp(drag,x_values,y_values))
    
    result = np.interp(prev_data,prev_scale_set,result_prev)

    return round(result,1) #corrected fuel flow, 100s of lbs per hour per engine


def get_uncorrected_ias_endurance(gwt, pressure_alt):

    TOP_FOLDER = "Backend/chart_dig/completed-cruise/max-endurance-4-eng"
    DIG_FILE_NAME = "uncorrected-speed.dig"

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

    gwt_scale_set = []
    result_gwt = []

    for gwt_scale, xy_pair_gwt in data.items():
        xy_pair_gwt = data[gwt_scale]

        x_values = xy_pair_gwt["x"]
        y_values = xy_pair_gwt["y"]

        gwt_scale_set.append(gwt_scale)
        result_gwt.append(np.interp(pressure_alt,x_values,y_values))
    
    result = np.interp(gwt,gwt_scale_set,result_gwt)

    return result

def get_corrected_ias_endurancep1(prev_data, temp_dev):

    TOP_FOLDER = "Backend/chart_dig/completed-cruise/max-endurance-4-eng"
    DIG_FILE_NAME = "corrected-temp-dev.dig"

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

    prev_scale_set = []
    result_prev = []

    for gwt_scale, xy_pair_gwt in data.items():
        xy_pair_gwt = data[gwt_scale]

        x_values = xy_pair_gwt["x"]
        y_values = xy_pair_gwt["y"]

        prev_scale_set.append(gwt_scale)
        result_prev.append(np.interp(temp_dev,x_values,y_values))
    
    result = np.interp(prev_data,prev_scale_set,result_prev)

    return result

def get_corrected_ias_endurancep2(prev_data, drag):

    TOP_FOLDER = "Backend/chart_dig/completed-cruise/max-endurance-4-eng"
    DIG_FILE_NAME = "corrected-drag.dig"

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

    prev_scale_set = []
    result_prev = []

    for gwt_scale, xy_pair_gwt in data.items():
        xy_pair_gwt = data[gwt_scale]

        x_values = xy_pair_gwt["x"]
        y_values = xy_pair_gwt["y"]

        prev_scale_set.append(gwt_scale)
        result_prev.append(np.interp(drag,x_values,y_values))
    
    result = np.interp(prev_data,prev_scale_set,result_prev)

    return round(result) # fully corrected best IAS for endurance 
