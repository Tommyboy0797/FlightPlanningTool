import sqlite3

# user_input_country = ""

def database_handle_navdata():
    # user_input_country = user_input
    database_path = "database/nav_data.db" # path to database

    connect_to_db = sqlite3.connect(database_path) # connect to database using mentioned path
    cursor = connect_to_db.cursor() # create a cursor, which allows us to execute SQL commands


    # cursor.execute("SELECT * FROM airports WHERE iso_country = ?", (user_input_country,))

    # country_airports = cursor.fetchall()  # Gets all matching rows

    cursor.execute("SELECT lat, lon, icao FROM airports WHERE iso_country = 'GB'")

    all_airports = cursor.fetchall()


    connect_to_db.close()
    return [{"lat": lat, "lng": lng, "name": icao} for lat, lng, icao in all_airports]
