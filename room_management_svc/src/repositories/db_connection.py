import atexit
from contextlib import contextmanager
from typing import Generator

from psycopg2 import pool
from psycopg2.extensions import connection

from src.config import settings

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
)


@contextmanager
def get_db_connection() -> Generator[connection, None, None]:
    """Yield a connection from the pool and return it when done."""
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)


def close_connection_pool() -> None:
    """Function to close the connection pool."""
    if connection_pool:
        connection_pool.closeall()


# Register the close_connection_pool function to be called on exit
atexit.register(close_connection_pool)
