
# Import FastAPI class to create the web application
from fastapi import FastAPI
# Import the SQLAlchemy engine and Base class for database setup
from app.database import engine, Base
# Import the router object from the books API module
from app.api.v1.books import router as books_router

# This line creates all tables in the database that are defined as subclasses of Base (e.g., Book)
# If the tables already exist, nothing happens. This is how the app auto-creates tables on startup.
Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance with a title and version
app = FastAPI(title="Digital Book Library", version="1.0.0")

# Register the books_router under the /api/v1 path prefix
# This means all endpoints defined in books_router will be available under /api/v1/books
app.include_router(books_router, prefix="/api/v1")
