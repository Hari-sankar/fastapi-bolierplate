from contextlib import contextmanager

from app.core.config import Settings
import psycopg2
from psycopg2.extras import DictCursor

settings = Settings()

@contextmanager
def get_db():
    conn = psycopg2.pool.SimpleConnectionPool(minconn=3,maxconn=10,url=settings.DATABASE_URL)
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        yield cursor
    except Exception as error:
        raise error
    else:
        conn.commit()
    finally:
        cursor.close()
        conn.close()
