import random
import os
import re
import numpy as np
print(os.getcwd())
from Backend.py_utils import *
from Backend import perf_calc as perf_calc

aircraft_grossweight = perf_calc.aircraft_grossweight
takeoff_factor = perf_calc.takeoff_factor


TOP_FOLDER = "Backend/chart_dig/completed-takeoff/amax-takeoff"
DIG_FILE_NAME = "amax-speed-rotation.dig"

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


def get_rotation_speed(gross_wt, takeoff_factor, data):
        
    x_values = []
    y_values = []
    
    for this_gross_weight, this_scales_data in data.items():
        x_values.append(this_gross_weight)
        y_values.append(round(np.interp(takeoff_factor, this_scales_data["x"], this_scales_data["y"]), 2)) 
    print("rotationspeed: ",(np.interp(gross_wt, x_values, y_values)))     
    return round(np.interp(gross_wt, x_values, y_values))
    


    
