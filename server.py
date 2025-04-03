import logging
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
import requests
from Backend import weather
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Request, Depends

app = FastAPI()

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthz") == -1

# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

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
def handle_data(request: Request,gwt,get_to_factor,get_rwy_available, get_rwy_slope, rsc, rcr, atcsoper, asoper, dragindex, origin, runwy):
    gwt = float(gwt)

    rwy_hdg = database_handler.runway_heading(origin, runwy)
    windspeed = wind_calc.get_wind_speed(origin)
    tail_or_head = wind_calc.calc_winds(rwy_hdg, wind_calc.get_wind_hdg(origin))

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

class SendString(BaseModel):
    send_str:str

class SendNum(BaseModel):
    send_int:float


# endpoint to handle the origin
@app.post("/set_origin")
def set_origin(origin: SendString):

    return 

@app.post("/get_runways")
def get_rwys(origin: SendString):
    runways = {
        "origin_runways": database_handler.get_runways(origin.send_str),
        "af_latlng": database_handler.get_spec_airfield(origin.send_str)
    }
    return runways

@app.post("/return_runway")
def return_runway(runwy: SendString, origin: SendString):

    sids = {
        "sids": database_handler.get_sids(origin.send_str, runwy.send_str),
        "runway_data": database_handler.get_runway_data(origin.send_str, runwy.send_str)
    }
    return sids

@app.post("/return_sid")
def return_sid(select_sid: SendString, origin: SendString, runwy: SendString,):

    sid_waypoints = {
        "selected_sid_points": database_handler.send_sid_points(select_sid.send_str, origin.send_str, runwy.send_str),
        "origin_latlng": database_handler.get_spec_airfield(origin.send_str)
    }

    return sid_waypoints

@app.post("/return_arrival_airport")
def return_arrival_airport(arrival_airfield: SendString):

    arrival_data = {
        "arrival_runways": database_handler.get_runways(arrival_airfield.send_str),
        "arrival_latlng": database_handler.get_spec_airfield(arrival_airfield.send_str)
    }

    return arrival_data


@app.post("/handle_stars")
def handle_stars(selected_runway: SendString, arrival_airfield: SendString):

    star_data = {
        "arrival_stars": database_handler.get_stars(arrival_airfield.send_str, selected_runway.send_str),
    }


    return star_data

@app.post("/send_star_data")
def send_star_data(selected_star: SendString, arrival_airfield: SendString, arrival_runway: SendString):

    star_points = {
        "selected_star_data": database_handler.send_star_data(selected_star.send_str, arrival_airfield.send_str, arrival_runway.send_str)
    }
    return star_points


@app.post("/waypoint_info")
def waypoint_info(waypoint_name: SendString):

    waypoint_info = {
        "waypointdata": database_handler.waypoint_search(waypoint_name.send_str),
    }

    return waypoint_info


@app.post("/append_route")
def append_route(waypoint: SendString, origin: SendString, runwy: SendString, select_sid: SendString, selected_star: SendString,selected_runway: SendString, arrival_airfield: SendString):

    handle_route.add_waypoint(waypoint.send_str)

    route_data = {
        "route": handle_route.build_route(origin.send_str, runwy.send_str, select_sid.send_str, selected_star.send_str, selected_runway.send_str, arrival_airfield.send_str)
    }

    return route_data


@app.post("/airfield_data")
def airfield_data(origin: SendString, runwy: SendString ):

    af_data = {
        "runway_data": database_handler.get_runway_data(origin.send_str, runwy.send_str),
        "origin_latlng": database_handler.get_spec_airfield(origin.send_str)
    }
    return af_data

@app.post("/get_airways")
def get_airways(airway_value: SendString):

    airways = {
        "airway_info": database_handler.get_airways(airway_value.send_str)
    }

    return airways


@app.post("/entered_airfield")
def entered_airfield(airfield_name: SendString):

    airfield = {
        "airfield_data": database_handler.get_spec_airfield(airfield_name.send_str)
    }
    print(database_handler.get_spec_airfield(airfield_name.send_str))
    return airfield


@app.post("/airfield_autocomplete")
def airfield_autocomplete(entered_text: SendString):

    result = {
        "autocorrect_data": database_handler.search_airport(entered_text.send_str)
    }

    return result

@app.post("/weather_info")
def weather_info(station_icao: SendString):

    weather_data = {
        "raw_metar": weather.get_metar(station_icao.send_str),
        "time": weather.get_wx_info(station_icao.send_str, "time"),
        "remarks": weather.get_wx_info(station_icao.send_str, "remarks"),
        "station": station_icao.send_str,
        "altimeter": f"{weather.get_wx_info(station_icao.send_str, 'altimeter')} hPa", 
        "temp": f"{weather.get_wx_info(station_icao.send_str, 'temperature')}°C",
        "humidity": weather.get_wx_info(station_icao.send_str, "humidity"),
        "dewpoint": f"{weather.get_wx_info(station_icao.send_str, 'dew_point')}°C", 
        "visibility": f"{weather.get_wx_info(station_icao.send_str, 'visibility')} SM", 
        "clouds": weather.get_wx_info(station_icao.send_str, "clouds"),
        "wind": f"{wind_calc.get_wind_hdg(station_icao.send_str)} / {wind_calc.get_wind_speed(station_icao.send_str)}"
    }
    return weather_data


@app.post("/nearest_waypoints")
def nearest_waypoints(lat: SendNum, lng: SendNum):
    nearby = {
        "waypoints": database_handler.nearby_points(lat.send_int, lng.send_int)
    }
    return nearby













## ----------------------------------------------- ## AUTHENTICATION ## ----------------------------------------------- ##

# Secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Initialize database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Password Hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Token Generation
def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

# Signup Route
@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return RedirectResponse(url="/", status_code=303)

# Login Route
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT hashed_password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row or not verify_password(password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(username)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True)
    return response

def verify_token(request: Request): # verify that they have a valid token and cant just bypass logging in
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Unable - Please log in")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # Return username if valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired, please log in again")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard_page(username: str = Depends(verify_token)):
    with open("Frontend/index.html", "r") as file:
        return HTMLResponse(content=file.read())
