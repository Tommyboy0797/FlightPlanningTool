from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Backend import perf_calc as perf_calc
from Backend import rotation_calc as rotation_calc
from Backend import refusal as refusal
from database import database_handler as db_handler
from fastapi.responses import JSONResponse
from Backend import handle_route as handle_route
from pydantic import BaseModel 

app = FastAPI()

templates = Jinja2Templates(directory="Frontend")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
def handle_data(request: Request,gwt,get_to_factor,get_rwy_available, get_rwy_slope):
    gwt = float(gwt)
    perf_calc.aircraft_grossweight = gwt
    respo = {
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

    }
       
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
        "large_airports": largeairports,
    })


class Origin(BaseModel): # class base model so that it knows what to expect
    airport_name:str #airport name set to string

class Rwy(BaseModel):
    selected_runway:str

class Sid(BaseModel):
    selected_sid:str

class Arrival(BaseModel):
    arrival_field:str

class ArrivalRunway(BaseModel):
    arrival_runway:str

class SelectedStar(BaseModel):
    selected_star:str

class WaypointName(BaseModel):
    waypointname:str

class WaypointAppend(BaseModel):
    waypoint:str

class AirfieldData(BaseModel):
    airfielddata:str

# endpoint to handle the origin
@app.post("/set_origin")
def set_origin(origin: Origin):

    airport_name = origin.airport_name
    print(airport_name)

    handle_route.origin_airfield = airport_name 
    handle_route.route = airport_name 

    print("print route",handle_route.route)
    print("print origin",handle_route.origin_airfield)

    return 

@app.get("/get_runways")
def get_rwys():
    origin_airfield = handle_route.origin_airfield
    runways = {
        "origin_runways": database_handler.get_runways(origin_airfield),
        "route": handle_route.route
    }
    return runways

@app.post("/return_runway")
def return_runway(runwy: Rwy):
    
    handle_route.selected_runway = runwy.selected_runway

    origin_airfield = handle_route.origin_airfield
    selected_runway = handle_route.selected_runway
    sids = {
        "sids": database_handler.get_sids(origin_airfield, selected_runway),
        "runway_data": database_handler.get_runway_data(handle_route.origin_airfield, handle_route.selected_runway)
    }
    return sids

@app.post("/return_sid")
def return_sid(select_sid: Sid):

    handle_route.selected_sid = select_sid.selected_sid
    print(f"Using the {handle_route.selected_sid} sid")

    print(f"function data:{database_handler.send_sid_points(handle_route.selected_sid, handle_route.origin_airfield, handle_route.selected_runway)}")
    sid_waypoints = {
        "selected_sid": handle_route.selected_sid,
        "selected_sid_points": database_handler.send_sid_points(handle_route.selected_sid, handle_route.origin_airfield, handle_route.selected_runway),
    }

    return sid_waypoints

@app.post("/return_arrival_airport")
def return_arrival_airport(arrival_airfield: Arrival):

    handle_route.arrival_airfield = arrival_airfield.arrival_field
    arrival_runways = database_handler.get_runways(handle_route.arrival_airfield)

    print(f"Arrival airport: {handle_route.arrival_airfield}")
    
    arrival_data = {
        "arrival_airfield": handle_route.arrival_airfield,
        "arrival_runways": arrival_runways,
        "route": handle_route.route
    }

    return arrival_data


@app.post("/handle_stars")
def handle_stars(selected_runway: ArrivalRunway):

    handle_route.selected_runway_arrival = selected_runway.arrival_runway

    star_data = {
        "selected_runway": handle_route.selected_runway_arrival,
        "arrival_stars": database_handler.get_stars(handle_route.arrival_airfield, handle_route.selected_runway_arrival),
        "route": handle_route.route
    }


    return star_data

@app.post("/send_star_data")
def send_star_data(selected_star: SelectedStar):

    handle_route.selected_star = selected_star.selected_star
    print(database_handler.send_star_data(handle_route.selected_star, handle_route.arrival_airfield))
    print("selected star: ", handle_route.selected_star)

    star_points = {
        "selected_star_data": database_handler.send_star_data(handle_route.selected_star, handle_route.arrival_airfield)
    }
    return star_points


@app.post("/waypoint_info")
def waypoint_info(waypoint_name: WaypointName):

    waypoint_info = {
        "waypointdata": database_handler.waypoint_search(waypoint_name.waypointname),
        "route": handle_route.route
    }

    return waypoint_info


@app.post("/append_route")
def append_route(waypoint: WaypointAppend):

    handle_route.add_waypoint(waypoint.waypoint)
    handle_route.build_route()
    print(handle_route.route)

    route_data = {
        "route": handle_route.route
    }

    return route_data


@app.get("/airfield_data")
def airfield_data():

    af_data = {
        "runway_data": database_handler.get_runway_data(handle_route.origin_airfield, handle_route.selected_runway)

    }
    return af_data

@app.post("/handle_winds")
def handle_winds():

    return