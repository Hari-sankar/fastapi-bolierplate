import subprocess
from app.db.session import get_db
import logging

def migration():
    try:
        logging.info("🚀 Starting database migration...")
        with get_db() as db:
            # Optional: check DB connection first
            try:
                db.execute("SELECT 1")  # Connection check
                logging.info(" DB connection successful.")
            except OperationalError as conn_err:
                logging.error(f" Failed to connect to DB: {conn_err}")
                return

            logging.info("Running Alembic migration via subprocess...")

            subprocess.run(
                ["alembic", "upgrade", "head"],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info(" Migration SQL executed successfully.")

    except subprocess.CalledProcessError as e:
         logging.error(" Alembic migration failed.")
         logging.error("STDOUT:", e.stdout)
         logging.error("STDERR:", e.stderr)

            # Execute the SQL script
    except Exception as e:
        logging.error(f" An error occurred during migration: {e}")
    finally:
        logging.info(" Database migration process complete.")




