# conftest.py: Global test fixtures for pytest
#
# IMPORTANT: DATABASE_URL must be set to SQLite BEFORE any app modules are imported,
# because app.database creates the engine at module level. Setting it here ensures
# pytest loads this before test files are collected.
import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test_temp.db"

# This file sets up:
# 1. A SQLite test database that overrides MySQL so tests never touch the real DB.
# 2. A global mock for the Google Books API using respx, so tests make no real HTTP requests.
#
# Both fixtures are autouse, so they apply automatically to all tests.

import pytest
import respx
from httpx import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+pysqlite:///./test_temp.db"

_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

# Create all tables in the test database once
Base.metadata.create_all(bind=_engine)


@pytest.fixture(autouse=True)
def override_get_db():
    # Override the FastAPI get_db dependency to use the SQLite test session
    def _get_db():
        db = _TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True, scope="session")
def mock_google_books_api():
    # Mock all Google Books API GET requests globally for all tests
    with respx.mock:
        respx.route(
            method="GET", url__startswith="https://www.googleapis.com/books/v1/volumes"
        ).mock(
            return_value=Response(
                200,
                json={
                    "items": [
                        {
                            "volumeInfo": {
                                "title": "Mocked Book",
                                "authors": ["Mock Author"],
                                "description": "Mocked description",
                            }
                        }
                    ]
                },
            )
        )
        yield
