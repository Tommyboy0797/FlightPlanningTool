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

def send_sid_points(selectedsid,origin):

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
        AND (waypoint_latitude IS NOT NULL OR center_waypoint_latitude IS NOT NULL)
        AND (waypoint_longitude IS NOT NULL OR center_waypoint_longitude IS NOT NULL)""", (selectedsid, origin))



    selected_sid = cursor.fetchall()

    connect_to_db.close()

    return [{"lat": latitude, "lng": longitude, "ident": waypoint_ident, "sequence_number": seqno} for latitude, longitude, waypoint_ident, seqno in selected_sid]