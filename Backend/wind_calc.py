from database import database_handler
from Backend import handle_route

def calc_winds(runwayhdg,windhdg):

    runwayhdg = int(runwayhdg[0][0]) # runwayhdg is a list, we get out a tuple with the first [0], then the value with the second

    windhdg = int(windhdg)

    tolerance = 30 # 30 degrees of tolerance

    diff = abs((windhdg - runwayhdg + 180) % 360 - 180)
    diff = diff <= tolerance

    if diff == True:
        print("Wind is headwind")
        return "Headwind"
    else:
        print("Wind is tail")
        return "Not headwind"



