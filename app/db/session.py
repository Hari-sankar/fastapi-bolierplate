import psycopg2
from psycopg2.extras import DictCursor
from app.core.config import Settings
from contextlib import contextmanager

settings = Settings()

@contextmanager
def get_db():
    conn = psycopg2.connect(settings.DATABASE_URL)
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