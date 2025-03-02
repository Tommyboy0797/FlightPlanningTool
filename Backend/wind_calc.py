from database import database_handler
from Backend import handle_route

def calc_winds(runwayhdg,windhdg):

    runwayhdg = int(runwayhdg[0][0]) # runwayhdg is a list, we get out a tuple with the first [0], then the value with the second

    windhdg = int(windhdg)

    tolerance = 30 # 30 degrees of tolerance

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



