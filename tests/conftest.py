# conftest.py: Global test fixtures for pytest
#
# This file sets up a global mock for the Google Books API using respx.
# All GET requests to 'https://www.googleapis.com/books/v1/volumes' (including any query parameters)
# will return a fixed mocked response. This ensures tests do not make real HTTP requests and
# always receive predictable data for Google Books API calls.
#
# The fixture is autouse and scoped to the session, so it applies to all tests automatically.

from httpx import Response
import pytest
import respx


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
