import os
from dotenv import load_dotenv
import redis


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
SQLALCHEMY_DATABASE_DEBUG = os.environ.get("DB_DEBUG", True)
SQLALCHEMY_DATABASE_URL = get_connection_string()
ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD", "admin")

# JWT Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")


# Redis settings
redishost = os.environ.get("REDIS_HOST", "redis")
redisport = os.environ.get("REDIS_PORT", 6379)
redispass = os.environ.get("REDIS_PASS", "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")
redisdb = os.environ.get("REDIS_DB", 0)

# Initialize Redis connection
redis_client = redis.Redis(
    host=redishost,
    port=redisport,
    db=redisdb,
    password=redispass,
    decode_responses=True
)

# Test connection
redis_client.set('foo', 'bar2')
value = redis_client.get('foo')  # Should return 'bar2'
print(value)