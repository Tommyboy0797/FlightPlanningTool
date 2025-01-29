import random
import os
import re
import numpy as np
print(os.getcwd())
from Backend.py_utils import *



aircraft_grossweight = 1
takeoff_factor = 1
rwy_available = 0 

TOP_FOLDER = "Backend/chart_dig/completed-takeoff/min-field-length-for-max-effort-to"
DIG_FILE_NAME = "amax-eff-uncorr-field-length.dig"

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

def try_get_uncorrected_max_eff_field_length(gross_wt, takeoff_factor, data):
        
    x_values = []
    y_values = []
    
    for this_gross_weight, this_scales_data in data.items():
        
        x_values.append(this_gross_weight)
        y_values.append(round(np.interp(takeoff_factor, this_scales_data["x"], this_scales_data["y"]), 2))       
    return round(np.interp(gross_wt, x_values, y_values), 2) * 1000
    


    
