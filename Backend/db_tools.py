from datetime import datetime, timedelta
import logging
import sqlite3
from jose import jwt
from passlib.context import CryptContext
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

DB_PATH = "/data/users.db"
# DB_PATH = "database/users.db"

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