from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Backend import perf_calc as perf_calc
from Backend import rotation_calc as rotation_calc
from Backend import refusal as refusal
from database import database_handler
from fastapi.responses import JSONResponse
from Backend import handle_route as handle_route
from pydantic import BaseModel 
from Backend import wind_calc

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

@app.get("/healthz")
def healthcheck():
    # Dont remove this. If you do, the website will not deploy.
    return 'ok'

# endpoint to recieve value for gross weight
@app.get("/get_data") # mailbox (what we are listening on), get is request type -> serving get 
def handle_data(request: Request,gwt,get_to_factor,get_rwy_available, get_rwy_slope, rsc, rcr, atcsoper, asoper, dragindex,windspeed,tail_or_head):
    gwt = float(gwt)

    p1 = refusal.get_refusal_p1(get_to_factor, get_rwy_available)
    p2 = refusal.get_refusal_p2(p1, gwt)
    p3 = refusal.get_refusal_p3(p2, get_rwy_slope)
    p4 = refusal.get_refusal_p4(p3, windspeed, tail_or_head)
    p5 = refusal.get_refusal_p5(p4, dragindex)
    p6 = refusal.get_refusal_p6(p5, rcr)
    p7 = refusal.get_refusal_p7(p6, rsc)
    p8 = refusal.get_refusal_p8(p7, atcsoper)
    p9 = refusal.get_refusal_p9(p8, asoper) 
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
        "corrected_refusal_speed": p9,
    }
       
    return respo

# endpoint for airports
@app.get("/fetch_airports")
def fetch_airports():
    mediumairports = database_handler.get_medium_airfields()
    largeairports = database_handler.get_large_airfields()
    smallairports = database_handler.get_small_airfields()
    
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

class WindHdg(BaseModel):
    windhdg:str

class Airway(BaseModel):
    airway_value:str


# endpoint to handle the origin
@app.post("/set_origin")
def set_origin(origin: Origin):
 
    return 

@app.post("/get_runways")
def get_rwys(origin: Origin):
    runways = {
        "origin_runways": database_handler.get_runways(origin.airport_name),
    }
    return runways

@app.post("/return_runway")
def return_runway(runwy: Rwy, origin: Origin):

    sids = {
        "sids": database_handler.get_sids(origin.airport_name, runwy.selected_runway),
        "runway_data": database_handler.get_runway_data(origin.airport_name, runwy.selected_runway)
    }
    return sids

@app.post("/return_sid")
def return_sid(select_sid: Sid, origin: Origin, runwy: Rwy,):

    sid_waypoints = {
        "selected_sid_points": database_handler.send_sid_points(select_sid.selected_sid, origin.airport_name, runwy.selected_runway),
    }

    return sid_waypoints

@app.post("/return_arrival_airport")
def return_arrival_airport(arrival_airfield: Arrival):

    arrival_data = {
        "arrival_runways": database_handler.get_runways(arrival_airfield.arrival_field),
    }

    return arrival_data


@app.post("/handle_stars")
def handle_stars(selected_runway: ArrivalRunway, arrival_airfield: Arrival):

    star_data = {
        "arrival_stars": database_handler.get_stars(arrival_airfield.arrival_field, selected_runway.arrival_runway),
    }


    return star_data

@app.post("/send_star_data")
def send_star_data(selected_star: SelectedStar, arrival_airfield: Arrival, arrival_runway: ArrivalRunway):

    star_points = {
        "selected_star_data": database_handler.send_star_data(selected_star.selected_star, arrival_airfield.arrival_field, arrival_runway.arrival_runway)
    }
    return star_points


@app.post("/waypoint_info")
def waypoint_info(waypoint_name: WaypointName):

    waypoint_info = {
        "waypointdata": database_handler.waypoint_search(waypoint_name.waypointname),
    }

    return waypoint_info


@app.post("/append_route")
def append_route(waypoint: WaypointAppend, origin: Origin, runwy: Rwy, select_sid: Sid,selected_star: SelectedStar,selected_runway: ArrivalRunway,arrival_airfield: Arrival):

    handle_route.add_waypoint(waypoint.waypoint)

    route_data = {
        "route": handle_route.build_route(origin.airport_name, runwy.selected_runway, select_sid.selected_sid, selected_star.selected_star, selected_runway.arrival_runway, arrival_airfield.arrival_field)
    }

    return route_data


@app.post("/airfield_data")
def airfield_data(origin: Origin, runwy: Rwy ):

    af_data = {
        "runway_data": database_handler.get_runway_data(origin.airport_name, runwy.selected_runway)
    }
    return af_data

@app.post("/handle_winds")
def handle_winds(windhdg: WindHdg, origin: Origin, runwy: Rwy ):

    rwy_hdg = database_handler.runway_heading(origin.airport_name, runwy.selected_runway)
    wind_data = {
        "head_or_tail_wind": wind_calc.calc_winds(rwy_hdg, windhdg.windhdg)
    }

    return wind_data


@app.post("/get_airways")
def get_airways(airway_value: Airway):

    airways = {
        "airway_info": database_handler.get_airways(airway_value.airway_value)
    }

    return airways


@app.post("/entered_airfield")
def entered_airfield(airfield_name: Origin):

    airfield = {
        "airfield_data": database_handler.get_spec_airfield(airfield_name.airport_name)
    }
    print(database_handler.get_spec_airfield(airfield_name.airport_name))
    return airfield


@app.post("/airfield_autocomplete")
def airfield_autocomplete(entered_text: Origin):

    result = {
        "autocorrect_data": database_handler.search_airport(entered_text.airport_name)
    }

    return result