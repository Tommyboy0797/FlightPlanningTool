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