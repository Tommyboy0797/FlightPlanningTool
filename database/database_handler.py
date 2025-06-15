import sqlite3
from Backend import handle_route 
from math import cos, asin, sqrt, pi


def get_small_airfields():
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT lat, lon, icao, type FROM airports WHERE type = 'small_airport'") # remove WHERE ..., added to improve performance, only loading UK airfields

    all_airports = cursor.fetchall()

    connect_to_db.close() # close database connection

    return [{"lat": lat, "lng": lng, "name": icao, "type": type} for lat, lng, icao, type in all_airports] #return airfield info 


def get_medium_airfields():
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT lat, lon, icao, type FROM airports WHERE type = 'medium_airport'") # remove WHERE ..., added to improve performance, only loading UK airfields

    all_airports = cursor.fetchall()

    connect_to_db.close() # close database connection

    return [{"lat": lat, "lng": lng, "name": icao, "type": type} for lat, lng, icao, type in all_airports] #return airfield info 


def get_large_airfields():
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT lat, lon, icao, type FROM airports WHERE type = 'large_airport'") # remove WHERE ..., added to improve performance, only loading UK airfields

    all_airports = cursor.fetchall()

    connect_to_db.close() # close database connection

    return [{"lat": lat, "lng": lng, "name": icao, "type": type} for lat, lng, icao, type in all_airports] #return airfield info 


def get_sids(origin,runway):
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT DISTINCT procedure_identifier FROM sids WHERE airport_identifier = ? AND transition_identifier = ?", (origin,runway))

    sids = cursor.fetchall()

    connect_to_db.close()

    return sids


def get_runways(origin):
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT 'RW' || name AS runway_name FROM runways WHERE icao = ?", (origin,))

    rwys = cursor.fetchall()

    connect_to_db.close()

    return rwys

def get_runway_data(origin, runway):

    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    runway_cleaned = runway.lstrip("RW")

    cursor.execute("SELECT length_ft, width_ft, hdg, surface FROM runways WHERE icao = ? AND name = ?", (origin,runway_cleaned,))

    rwys = cursor.fetchall()

    connect_to_db.close()

    return [{"length": length_ft, "width": width_ft, "hdg": hdg, "surface": surface} for length_ft, width_ft, hdg, surface in rwys]

def send_sid_points(selectedsid,origin,runway):

    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("""
        SELECT 
            CASE 
                WHEN waypoint_latitude IS NOT NULL THEN waypoint_latitude 
                ELSE center_waypoint_latitude 
            END AS latitude,
            CASE 
                WHEN waypoint_longitude IS NOT NULL THEN waypoint_longitude 
                ELSE center_waypoint_longitude 
            END AS longitude,
            waypoint_identifier, 
            seqno
        FROM sids 
        WHERE procedure_identifier = ?
        AND airport_identifier = ?
        AND transition_identifier = ?
        AND (waypoint_latitude IS NOT NULL OR center_waypoint_latitude IS NOT NULL)
        AND (waypoint_longitude IS NOT NULL OR center_waypoint_longitude IS NOT NULL)""", (selectedsid, origin,runway))



    selected_sid = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_ident, "sequence_number": seqno} for latitude, longitude, waypoint_ident, seqno in selected_sid]


def get_stars(arrival,runway):

    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT DISTINCT procedure_identifier FROM stars WHERE airport_identifier = ? AND (transition_identifier = ? OR transition_identifier = 'ALL')", (arrival,runway))

    stars = cursor.fetchall()

    connect_to_db.close()

    return stars



def send_star_data(procedure, airport, runway):

    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands
    
    cursor.execute("""
        SELECT 
            CASE 
                WHEN waypoint_latitude IS NOT NULL THEN waypoint_latitude 
                ELSE center_waypoint_latitude 
            END AS latitude,
            CASE 
                WHEN waypoint_longitude IS NOT NULL THEN waypoint_longitude 
                ELSE center_waypoint_longitude 
            END AS longitude,
            waypoint_identifier, 
            seqno
        FROM stars
        WHERE procedure_identifier = ?
        AND airport_identifier = ?
        AND (transition_identifier = ? OR transition_identifier = (
            SELECT transition_identifier 
            FROM stars
            WHERE procedure_identifier = ?
            AND airport_identifier = ?
            LIMIT 1
        ))
        AND (waypoint_latitude IS NOT NULL OR center_waypoint_latitude IS NOT NULL)
        AND (waypoint_longitude IS NOT NULL OR center_waypoint_longitude IS NOT NULL)
    """, (procedure, airport, runway, procedure, airport))

    selected_star = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_ident, "sequence_number": seqno} for latitude, longitude, waypoint_ident, seqno in selected_star]


def waypoint_search(waypointname):
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("""SELECT DISTINCT waypoint_latitude, waypoint_longitude, waypoint_identifier, waypoint_name, waypoint_usage, icao_code, area_code FROM waypoints WHERE waypoint_identifier = ? OR waypoint_name = ?""", (waypointname, waypointname))

    waypoint_info = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_identifier, "name": waypoint_name, "usage": waypoint_usage, "icao": icao_code, "area": area_code} for latitude, longitude, waypoint_identifier, waypoint_name, waypoint_usage, icao_code, area_code in waypoint_info]


def runway_heading(airfield, runway):

    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    runway_cleaned = runway.lstrip("RW")

    cursor.execute("SELECT hdg FROM runways WHERE icao = ? AND name = ?", (airfield,runway_cleaned))

    runway_hdg = cursor.fetchall()

    connect_to_db.close()

    return runway_hdg


def get_airways(airway_number):
    
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute(""" SELECT waypoint_latitude, waypoint_longitude, waypoint_identifier, outbound_course, inbound_course, inbound_distance, route_identifier, seqno FROM airways WHERE route_identifier = ?""",(airway_number,))

    airway_info = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": waypoint_latitude, "lng": waypoint_longitude, "ident": waypoint_identifier, "ob_course": outbound_course, "ib_course": inbound_course, "ib_dist": inbound_distance, "route_ident": route_identifier, "seqno": seqno} for waypoint_latitude, waypoint_longitude, waypoint_identifier, outbound_course, inbound_course, inbound_distance, route_identifier, seqno in airway_info]


def get_spec_airfield(airfield_name):
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("SELECT lat, lon, icao, type FROM airports WHERE icao = ?", (airfield_name,))

    airfield = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": lat, "lng": lng, "name": icao, "type": type} for lat, lng, icao, type in airfield]

def search_airport(partial_name):
    database_path = "database/nav_data.db"
    connect_to_db = sqlite3.connect(database_path)
    cursor = connect_to_db.cursor()

    words = partial_name.split()
    conditions = " AND ".join(["name LIKE ? COLLATE NOCASE" for _ in words])

    query = f"""
    SELECT name, icao,type
    FROM airports 
    WHERE {conditions} 
    ORDER BY 
        LENGTH(name), 
        INSTR(LOWER(name), LOWER(?)) 
    """

    params = tuple(f"%{word}%" for word in words) + (words[0],)

    cursor.execute(query, params)
    results = cursor.fetchall()
    connect_to_db.close()

    return [{"name": name, "icao": icao, "type": type,} for name, icao, type in results]


# autocorrect suggestions for gps waypoint box
def search_waypoint(partial_name):
    database_path = "database/nav_data.db"
    connect_to_db = sqlite3.connect(database_path)
    cursor = connect_to_db.cursor()

    words = partial_name.split()
    conditions = " AND ".join(["waypoint_name LIKE ? COLLATE NOCASE" for _ in words])

    query = f"""
    SELECT waypoint_latitude, waypoint_longitude, waypoint_identifier, waypoint_name, waypoint_usage, icao_code, area_code
    FROM waypoints 
    WHERE {conditions} 
    ORDER BY 
        LENGTH(waypoint_name), 
        INSTR(LOWER(waypoint_name), LOWER(?)) 
    """

    params = tuple(f"{word}%" for word in words) + (words[0],) # only get waypoints that START with partial_name

    cursor.execute(query, params)
    results = cursor.fetchall()
    connect_to_db.close()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_identifier, "name": waypoint_name, "usage": waypoint_usage, "icao": icao_code, "area": area_code} for latitude, longitude, waypoint_identifier, waypoint_name, waypoint_usage, icao_code, area_code in results]



def nearby_points(point_lat, point_lng):
    database_path = "database/nav_data.db"
    connect_to_db = sqlite3.connect(database_path)
    cursor = connect_to_db.cursor()

    cursor.execute("SELECT waypoint_identifier, waypoint_latitude, waypoint_longitude FROM waypoints")

    close_wp = []

    data = cursor.fetchall()

    def distance(lat1, lon1, lat2, lon2):
        r = 3958.8 # miles
        p = pi / 180

        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 2 * r * asin(sqrt(a))
    
    for waypoint in data:
        waypoint_id, waypoint_lat, waypoint_lng = waypoint
        dist = distance(point_lat, point_lng, waypoint_lat, waypoint_lng)
        dist = round(dist)
        if dist < 20:
            close_wp.append([waypoint_id,waypoint_lat,waypoint_lng, dist])
    
    return [{"name": name, "lat": lat, "lng": lng, "dist": dist} for name, lat, lng, dist in close_wp]

