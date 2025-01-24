# Manages the database connection and session.
# It includes SQLAlchemy engine and session setup for PostgreSQL.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
    


load_dotenv()
DATABASE_URL=os.getenv('DATABASE_URL');
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()
def test_connection():
    try:
        # Try to connect to the database
        with engine.connect() as connection:
            print("Database connection successful!")
            return True
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return False

