import os

import redis
from dotenv import load_dotenv

load_dotenv()


def redis_connection():
    return redis.Redis(
        host=os.getenv('REDIS_HOST', default='localhost'),
        port=os.getenv('REDIS_PORT', default=6379),
        db=os.getenv('REDIS_DB', default=0),
    )
