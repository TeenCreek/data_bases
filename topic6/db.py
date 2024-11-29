import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

load_dotenv()

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    cursor_factory=RealDictCursor,
)


def get_connection():
    """Установка соединения с БД."""

    return pool.getconn()


def release_connection(conn):
    """Возврат соединения в пул."""

    pool.putconn(conn)


def close_pool():
    """Закрытие всех соединений в пуле."""

    pool.closeall()
