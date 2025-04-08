from datetime import datetime, timedelta
import logging
import sqlite3
from jose import jwt
from passlib.context import CryptContext
import os
## ----------------------------------------------- ## AUTHENTICATION ## ----------------------------------------------- ##
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
logFormatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s"
    )
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
LOGGER.addHandler(consoleHandler)
LOGGER.propagate = False

# Secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

DB_PATH = "database/users.db"
try:
    # Check for environment var. This will only be set 
    # in prod. Otherwise, leave user db path alone.
    if os.environ["IS_PROD"]:
        LOGGER.info("Database is running in prod... setting to /data/users.db")
        DB_PATH = "/data/users.db"
except KeyError:
    pass

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize database
def init_db():
    LOGGER.info('Initializing database')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_routes (
            username TEXT,
            route_number INTEGER,
            route_data TEXT,
            PRIMARY KEY(username, route_number),
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    cursor.execute("CREATE TABLE IF NOT EXISTS users (signup_date TEXT)")
    conn.commit()
    conn.close()
    LOGGER.info('Database setup complete')

def decode_token(token: str) ->str:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# Password Hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Token Generation
def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def get_account_info(username: str):
    """
    Get signup date for a single username
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT signup_date FROM users WHERE username=?", (username,))
    data = cursor.fetchone()
    return {"user": username, "signup_date": data[0]}
    
def store_route(route, username):

    freeslot = None
    taken_slots = set() # needs to be an empty set not "None"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT route_number FROM user_routes WHERE username = ?", (username,)) # gets all taken slots in db for that user
    for row in cursor.fetchall():
        taken_slots.add(row[0])
        print(f"row: {row}")
        print(f"taken slots: {taken_slots}") # puts all taken slots in a variable

    for slot in range(1,11):
        if slot not in taken_slots:
            freeslot = slot # finds the next free slot
            print(f"free slot is: {freeslot}")
            break # escape loop

    if freeslot == None: # if there is no free spaces
        print("NO FREE SLOT FOUND IN DB TO SAVE ROUTE")

    cursor.execute("INSERT INTO user_routes (username, route_number, route_data) VALUES (?,?,?)", (username, freeslot, route)) # put the data in 

    conn.commit()
    conn.close()
    
    return freeslot


def get_saved_routes(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT route_number, route_data FROM user_routes WHERE username = ? ORDER BY route_number", (username,))
    rows = cursor.fetchall()
    conn.close()

    routes = []
    for route_number, route_data in rows:
        route_parts = route_data.strip().split()
        from_airport = route_parts[0] if len(route_parts) > 0 else ""
        to_airport = route_parts[-1] if len(route_parts) > 1 else ""

        routes.append({
            "route_name": f"Route {route_number}",
            "from": from_airport,
            "to": to_airport,
            "last_used": "Just now",  # update later with timestamb
            "route_data": route_data
        })

    return {"routes": routes}

import sqlite3

def remove_route(username, routename):
    # Check if the routename is in the expected format (e.g., "Route 1")
    if not routename.startswith("Route ") or len(routename.split()) != 2:
        return {"status": "error", "message": "Invalid route name format."}
    
    # Extract the route number from the routename (e.g., "Route 1" becomes 1)
    try:
        route_number = int(routename.split()[1])
    except ValueError:
        return {"status": "error", "message": "Invalid route number."}
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete the route from the user_routes table
    cursor.execute("DELETE FROM user_routes WHERE username = ? AND route_number = ?", (username, route_number))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return {"status": "success", "message": f"Route {route_number} deleted."}
