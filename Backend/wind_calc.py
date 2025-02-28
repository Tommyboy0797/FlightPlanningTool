from database import database_handler
from Backend import handle_route

def calc_winds(airport,runwayhdg,windspeed,windhdg):

    runway_hdg = database_handler.runway_heading(airport,runwayhdg)

    tolerance = 30

    diff = abs((windhdg - runwayhdg + 180) % 360 - 180)
    diff = diff <= tolerance

    if diff == True:
        print("Wind is headwind")
    else:
        print("Wind is tail")

    return 


