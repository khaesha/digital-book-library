# Standard library for environment variables
import os

# SQLAlchemy imports for database engine and ORM base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# dotenv allows loading environment variables from a .env file
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Get the database connection URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine (handles DB connections)
engine = create_engine(DATABASE_URL)
# Create a session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all ORM models (tables)
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI routes: yields a database session
# Ensures the session is closed after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
