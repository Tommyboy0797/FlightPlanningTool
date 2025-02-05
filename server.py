from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from Backend import perf_calc as perf_calc
from Backend import rotation_calc as rotation_calc
from Backend import refusal as refusal
from database import database_handler as db_handler
from fastapi.responses import JSONResponse
from Backend import handle_route as handle_route
from pydantic import BaseModel 

app = FastAPI()

templates = Jinja2Templates(directory="Frontend")

@app.get("/")
def read_root(request: Request):
    respo = templates.TemplateResponse(
        "index.html", 
        {"request": request,
          "title": "TOLD TEST",
            }

        
    )
    return respo


# endpoint to recieve value for gross weight
@app.get("/get_data") # mailbox (what we are listening on), get is request type -> serving get 
def handle_data(request: Request,gwt,get_to_factor,get_rwy_available, get_rwy_slope, enter_db_country):
    gwt = float(gwt)
    perf_calc.aircraft_grossweight = gwt
    print(gwt)
    respo = templates.TemplateResponse(
        "index.html", 
        {"request": request,
            "uncorrected_max_eff_TO_dist_text": "Uncorrected maximum effort takeoff distance: ",
            "uncorrected_max_eff_TO_dist": perf_calc.try_get_uncorrected_max_eff_field_length(gwt, get_to_factor, perf_calc.data),
            "gross_weight_text": round(gwt * 1000),
            "takeoff_factor_text": get_to_factor,
            "rotation_speed_calculated": rotation_calc.get_rotation_speed(gwt, get_to_factor, rotation_calc.data),
            "runway_avail": get_rwy_available,
            "uncorrected_refusal_test": refusal.get_refusal_p1(get_to_factor, get_rwy_available),
            "uncorrected_refusal_test_p2": refusal.get_refusal_p2(refusal.get_refusal_p1(get_to_factor, get_rwy_available), gwt),
            "partially_corrected_refusal_p3": refusal.get_refusal_p3(refusal.get_refusal_p2(refusal.get_refusal_p1(get_to_factor, get_rwy_available), gwt), get_rwy_slope),
            "runway_slope": refusal.rwy_slope,
            "user_route": handle_route.route,
            }
    )
        
    
    return respo


# endpoint for airports
@app.get("/fetch_airports")
def fetch_airports():
    mediumairports = db_handler.get_medium_airfields()
    largeairports = db_handler.get_large_airfields()
    smallairports = db_handler.get_small_airfields()
    
    return JSONResponse(content={
        "small_airports": smallairports,
        "medium_airports": mediumairports,
        "large_airports": largeairports
    })


class Origin(BaseModel):
    airport_name:str



# endpoint to handle the origin
@app.post("/set_origin")
def set_origin(origin: Origin):

    airport_name = origin.airport_name
    print(airport_name)

    handle_route.origin_airfield = airport_name 
    handle_route.route = airport_name     
    print("print route",handle_route.route)
    print("print origin",handle_route.origin_airfield)

    return {
        "request": origin,
        "user_route": handle_route.route,
    }
