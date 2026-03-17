import pytest
from fastapi.testclient import TestClient
from app.main import app

import respx
from httpx import Response

client = TestClient(app)


def test_ocr_book_cover_success(monkeypatch):
    # Mock OCR extraction
    def mock_extract_book_info_from_image(file):
        return {
            "title": "Mocked Title",
            "author": "Mocked Author",
            "raw_text": "Mocked Title Mocked Author",
        }

    monkeypatch.setattr(
        "app.services.ocr.extract_book_info_from_image",
        mock_extract_book_info_from_image,
    )

    # Simulate file upload
    response = client.post(
        "/books/ocr", files={"file": ("test.jpg", b"fake image bytes", "image/jpeg")}
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
