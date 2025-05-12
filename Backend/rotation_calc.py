import random
import os
import re
import numpy as np
print(os.getcwd())
from Backend.py_utils import *
from Backend import perf_calc as perf_calc

def get_rotation_speed(gross_wt, takeoff_factor):
    TOP_FOLDER = "Backend/chart_dig/completed-takeoff/amax-takeoff"
    DIG_FILE_NAME = "amax-speed-rotation.dig"

    # Parse the dig file
    data = {}
    chart = ParseDig(f'./{TOP_FOLDER}/dig/{DIG_FILE_NAME}')
    for c in chart.curveNames():
        yVector = [row[1] for row in chart.curve(c)]
        xVector = [row[0] for row in chart.curve(c)]
        scale_number = float(re.sub('[^0-9]', '', c.replace("-", "_")))

        data[scale_number] = {
            "x": xVector,
            "y": yVector
        }

    # Prepare the interpolation arrays
    weight_scale_set = []  # Gross weight scale (e.g., 30000, 40000, 50000)
    results_based_on_to_factor = []  # Rotation speed for each gross weight based on takeoff factor

    for weight_scale, xy_pairs in data.items():
        x_values = xy_pairs["x"]
        y_values = xy_pairs["y"]

        weight_scale_set.append(weight_scale)
        results_based_on_to_factor.append(round(np.interp(takeoff_factor, x_values, y_values), 2))

    # Interpolate for the given gross weight
    rotation_speed = np.interp(gross_wt, weight_scale_set, results_based_on_to_factor)

    return round(rotation_speed)

    
