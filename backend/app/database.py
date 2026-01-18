from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./database.db')
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        if inspector.has_table("product"):
            columns = [c["name"] for c in inspector.get_columns("product")]
            if "min_quantity" not in columns:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE product ADD COLUMN min_quantity INTEGER DEFAULT 0"))
    except Exception as e:
        print(f"Migration warning: {e}")

def get_session():
    with Session(engine) as session:
        yield session