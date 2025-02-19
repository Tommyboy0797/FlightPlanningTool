import sqlite3
from Backend import handle_route 


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

    cursor.execute("SELECT DISTINCT transition_identifier FROM sids WHERE transition_identifier LIKE 'RW%' AND airport_identifier = ?", (origin,))

    rwys = cursor.fetchall()

    connect_to_db.close()

    return rwys

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



def send_star_data(procedure, airport):

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
            AND (waypoint_latitude IS NOT NULL OR center_waypoint_latitude IS NOT NULL)
            AND (waypoint_longitude IS NOT NULL OR center_waypoint_longitude IS NOT NULL)                 
                   """, (procedure, airport))



    selected_star = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_ident, "sequence_number": seqno} for latitude, longitude, waypoint_ident, seqno in selected_star]


def waypoint_search(waypointname):
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands

    cursor.execute("""SELECT DISTINCT waypoint_latitude, waypoint_longitude, waypoint_identifier, waypoint_name, waypoint_usage, icao_code, area_code FROM waypoints WHERE waypoint_identifier = ? OR waypoint_name = ?""", (waypointname, waypointname))

    waypoint_info = cursor.fetchall()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_identifier, "name": waypoint_name, "usage": waypoint_usage, "icao": icao_code, "area": area_code} for latitude, longitude, waypoint_identifier, waypoint_name, waypoint_usage, icao_code, area_code in waypoint_info]