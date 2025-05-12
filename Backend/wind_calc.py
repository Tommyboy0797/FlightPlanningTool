from database import database_handler
from Backend import handle_route
import requests

def calc_winds(runwayhdg,windhdg):

    if windhdg == None: # variable wind direction
        windhdg = "0"

    if not runwayhdg or not runwayhdg[0]:
        runwayhdg = [[0]] # default north if there is not a selected runway yet
        
    runwayhdg = int(runwayhdg[0][0]) # runwayhdg is a list, we get out a tuple with the first [0], then the value with the second

    windhdg = int(windhdg)

    tolerance = 30 # degrees of tolerance

    diff = abs((windhdg - runwayhdg + 180) % 360 - 180)
    diff = diff <= tolerance

    reciprocal_hdg = (runwayhdg + 180) % 360 # get the recirpocal heading of the runway
    undiff = abs((windhdg - reciprocal_hdg + 180) % 360 - 180)
    tailwind = undiff <= tolerance

    if diff == True:
        return "Headwind"
    elif tailwind == True:
        return "Tailwind"
    else:
        return "Crosswind"


def get_wind_hdg(icao):
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": "NqeMiDKymD4VjT9epVakwJrQgBkDLutjqymAw2vFkoM"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["wind_direction"]["value"]
    return 0

def get_wind_speed(icao):
    url = f"https://avwx.rest/api/metar/{icao}"
    headers = {"Authorization": "NqeMiDKymD4VjT9epVakwJrQgBkDLutjqymAw2vFkoM"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["wind_speed"]["value"]
    return 0

