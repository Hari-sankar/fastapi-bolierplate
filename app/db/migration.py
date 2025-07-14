from app.db.session import get_db
import logging

def migration():
    try:
        # Read SQL file
        with open("app/db/migration.sql", 'r') as file:
            sql_file_content = file.read()
    except FileNotFoundError:
        logging.error(f"File migration.sql not found")
        return
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        return

    try:
        # Initialize the Database
        logging.info("Database Migration Intiated")
        with get_db() as db:
            db.execute(sql_file_content)
    except Exception as e:
        logging.error(f"An error occurred while executing the SQL: {e}")
    finally:
        logging.info("Database Migration Completed")
