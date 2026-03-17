# Import FastAPI class to create the web application
from fastapi import FastAPI

# Import the SQLAlchemy engine and Base class for database setup
from app.database import engine, Base

# Import the router object from the books API module
from app.api.v1.books import router as books_router

# Import the healthcheck router
from app.api.v1.healthcheck import router as healthcheck_router

# Import custom middlewares
from app.middlewares.error_catch import ErrorCatchMiddleware
from app.middlewares.rate_limit import RateLimitMiddleware
from app.middlewares.request_logging import RequestLoggingMiddleware


# This line creates all tables in the database that are defined as subclasses of Base (e.g., Book)
# If the tables already exist, nothing happens. This is how the app auto-creates tables on startup.
Base.metadata.create_all(bind=engine)


# Create the FastAPI application instance with a title and version
app = FastAPI(title="Digital Book Library", version="1.0.0")

# Register custom middlewares in order:
# 1. Error catching (outermost)
app.add_middleware(ErrorCatchMiddleware)
# 2. Rate limiting
app.add_middleware(RateLimitMiddleware)
# 3. Request logging (innermost)
app.add_middleware(RequestLoggingMiddleware)


# Register the books_router under the /api/v1 path prefix
# This means all endpoints defined in books_router will be available under /api/v1/books
app.include_router(books_router, prefix="/api/v1")

# Register the healthcheck router under the /api/v1 path
app.include_router(healthcheck_router, prefix="/api/v1")
