# Import datetime for timestamp fields
from datetime import datetime

# Import Pydantic's BaseModel for data validation and HttpUrl for URL type
from pydantic import BaseModel, HttpUrl


# Schema for creating a new book (request body)
class BookCreate(BaseModel):
    url: HttpUrl  # Only the URL is required from the user


# Schema for updating a book (partial update)
class BookUpdate(BaseModel):
    title: str | None = None  # Optional title
    description: str | None = None  # Optional description


# Schema for returning a book (response body)
class BookResponse(BaseModel):
    id: int  # Book ID
    url: str  # Book URL
    title: str | None  # Book title (optional)
    description: str | None  # Book description (optional)
    created_at: datetime  # Timestamp when the book was added

    # This config allows Pydantic to create a model from ORM objects
    model_config = {"from_attributes": True}


# Schema for OCR response (book cover image upload)
class BookOCRResponse(BaseModel):
    title: str | None
    author: str | None
    raw_text: str
    metadata: dict | None = None  # Optionally include fetched metadata
