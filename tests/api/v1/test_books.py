from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app

client = TestClient(app)

# Shared fake book data used across tests
FAKE_BOOK = MagicMock(
    id=1,
    url="https://example.com/book1",
    title="Book One",
    description="Desc one",
    created_at=datetime(2026, 1, 1),
)

FAKE_BOOKS = [
    FAKE_BOOK,
    MagicMock(
        id=2,
        url="https://example.com/book2",
        title="Book Two",
        description="Desc two",
        created_at=datetime(2026, 1, 2),
    ),
]


@pytest.fixture(autouse=True)
def mock_db(mocker):
    """Override FastAPI get_db dependency with a mock session for every test."""
    db = mocker.MagicMock()
    app.dependency_overrides[get_db] = lambda: db
    yield db
    app.dependency_overrides.pop(get_db, None)


# --- list_books ---


def test_list_books_pytest_mock(mocker):
    mocker.patch("app.api.v1.books.repo.get_all_books", return_value=FAKE_BOOKS)
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Book One"
    assert data[1]["title"] == "Book Two"


def test_list_books_unittest_mock():
    with patch("app.api.v1.books.repo.get_all_books", return_value=FAKE_BOOKS):
        response = client.get("/api/v1/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Book One"
    assert data[1]["title"] == "Book Two"


# --- add_book ---


def test_add_book_success(mocker):
    mocker.patch(
        "app.api.v1.books.fetch_metadata",
        new=mocker.AsyncMock(
            return_value={"title": "Fetched Title", "description": "Fetched Desc"}
        ),
    )
    mocker.patch("app.api.v1.books.repo.create_book", return_value=FAKE_BOOK)
    response = client.post("/api/v1/books", json={"url": "https://example.com/book1"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Book One"


# --- get_book ---


def test_get_book_success(mocker):
    mocker.patch("app.api.v1.books.repo.get_book_by_id", return_value=FAKE_BOOK)
    response = client.get("/api/v1/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Book One"


def test_get_book_not_found(mocker):
    mocker.patch("app.api.v1.books.repo.get_book_by_id", return_value=None)
    response = client.get("/api/v1/books/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


# --- update_book ---


def test_update_book_success(mocker):
    updated_book = MagicMock(
        id=1,
        url="https://example.com/book1",
        title="Updated Title",
        description="Updated Desc",
        created_at=datetime(2026, 1, 1),
    )
    mocker.patch("app.api.v1.books.repo.get_book_by_id", return_value=FAKE_BOOK)
    mocker.patch("app.api.v1.books.repo.update_book", return_value=updated_book)
    response = client.patch("/api/v1/books/1", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_update_book_not_found(mocker):
    mocker.patch("app.api.v1.books.repo.get_book_by_id", return_value=None)
    response = client.patch("/api/v1/books/99", json={"title": "Updated Title"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


# --- delete_book ---


def test_delete_book_success(mocker):
    mocker.patch("app.api.v1.books.repo.get_book_by_id", return_value=FAKE_BOOK)
    mocker.patch("app.api.v1.books.repo.delete_book")
    response = client.delete("/api/v1/books/1")
    assert response.status_code == 204


def test_delete_book_not_found(mocker):
    mocker.patch("app.api.v1.books.repo.get_book_by_id", return_value=None)
    response = client.delete("/api/v1/books/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


# --- ocr_book_cover ---


def test_ocr_book_cover_success(monkeypatch):
    def mock_extract_book_info_from_image(file):
        return {
            "title": "Mocked Title",
            "author": "Mocked Author",
            "raw_text": "Mocked Title Mocked Author",
        }

    # Patch at the import location in books.py, not the source module
    monkeypatch.setattr(
        "app.api.v1.books.extract_book_info_from_image",
        mock_extract_book_info_from_image,
    )

    # Simulate file upload — full path including /api/v1 prefix
    response = client.post(
        "/api/v1/books/ocr",
        files={"file": ("test.jpg", b"fake image bytes", "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Mocked Title"
    assert data["author"] == "Mocked Author"
    assert data["raw_text"] == "Mocked Title Mocked Author"
    assert data["metadata"]["items"][0]["volumeInfo"]["title"] == "Mocked Book"
    assert data["metadata"]["items"][0]["volumeInfo"]["authors"] == ["Mock Author"]
    assert (
        data["metadata"]["items"][0]["volumeInfo"]["description"]
        == "Mocked description"
    )


# --- Using pytest-mock (mocker fixture) ---
def test_list_books_pytest_mock(mocker):
    mock_db = mocker.MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    mocker.patch("app.api.v1.books.repo.get_all_books", return_value=FAKE_BOOKS)

    response = client.get("/api/v1/books")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Book One"
    assert data[1]["title"] == "Book Two"

    app.dependency_overrides.pop(get_db, None)


# --- Using unittest.mock ---
def test_list_books_unittest_mock():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db

    with patch("app.api.v1.books.repo.get_all_books", return_value=FAKE_BOOKS):
        response = client.get("/api/v1/books")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Book One"
    assert data[1]["title"] == "Book Two"

    app.dependency_overrides.pop(get_db, None)


def test_ocr_book_cover_success(monkeypatch):
    # Mock OCR extraction
    def mock_extract_book_info_from_image(file):
        return {
            "title": "Mocked Title",
            "author": "Mocked Author",
            "raw_text": "Mocked Title Mocked Author",
        }

    # Patch at the import location in books.py, not the source module
    monkeypatch.setattr(
        "app.api.v1.books.extract_book_info_from_image",
        mock_extract_book_info_from_image,
    )

    # Simulate file upload — full path including /api/v1 prefix
    response = client.post(
        "/api/v1/books/ocr",
        files={"file": ("test.jpg", b"fake image bytes", "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Mocked Title"
    assert data["author"] == "Mocked Author"
    assert data["raw_text"] == "Mocked Title Mocked Author"
    assert data["metadata"]["items"][0]["volumeInfo"]["title"] == "Mocked Book"
    assert data["metadata"]["items"][0]["volumeInfo"]["authors"] == ["Mock Author"]
    assert (
        data["metadata"]["items"][0]["volumeInfo"]["description"]
        == "Mocked description"
    )
