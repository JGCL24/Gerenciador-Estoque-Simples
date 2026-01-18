from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./database.db')
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # If the `min_quantity` column is missing (older DBs), add it safely for SQLite.
    # This uses PRAGMA table_info to inspect columns and adds the column with a default of 0 when necessary.
    try:
        from sqlalchemy import text
        with engine.begin() as conn:
            res = conn.exec_driver_sql("PRAGMA table_info('product')").all()
            cols = [r[1] for r in res]
            if 'min_quantity' not in cols:
                conn.exec_driver_sql("ALTER TABLE product ADD COLUMN min_quantity INTEGER DEFAULT 0")
    except Exception:
        # If migration fails, we swallow the error here and let normal create_all behavior continue.
        # In development you can delete the SQLite file (database.db) to recreate the schema.
        pass

def get_session():
    with Session(engine) as session:
        yield session
