import os
from dotenv import load_dotenv

load_dotenv()

def get_connection_string():
    dbengine = os.environ.get("DB_ENGINE", "postgresql")
    dbhost = os.environ.get("DB_HOST")
    dbport = os.environ.get("DB_PORT", "5432")
    dbusername = os.environ.get("DB_USERNAME")
    dbpassword = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")

    return f'{dbengine}://{dbusername}:{dbpassword}@{dbhost}:{dbport}/{dbname}'

# Database Setting
SQLALCHEMY_DATABASE_URL = get_connection_string()
ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD", "admin")

# JWT Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
