
# Import FastAPI utilities for routing, dependency injection, and error handling
from fastapi import APIRouter, Depends, HTTPException, status
# Import SQLAlchemy Session for database operations
from sqlalchemy.orm import Session
# Import the get_db dependency to get a database session
from app.database import get_db
# Import Pydantic schemas for request and response validation
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookOCRResponse
# Import the async metadata fetching service
from app.services.metadata import fetch_metadata
# Import the OCR service
# Import httpx for Google Books API call
from app.services.ocr import extract_book_info_from_image
import httpx
# Import CRUD functions for Book from the repository layer
import app.crud.book_repo as repo

# Create a router for all book-related endpoints, with a URL prefix and tag for docs
from fastapi import UploadFile, File
router = APIRouter(prefix="/books", tags=["books"])
# Endpoint to extract book info from an uploaded image (OCR)
# - Accepts an image file upload
# - Extracts title/author using EasyOCR
# - Fetches metadata using extracted title

# Updated OCR endpoint to use Google Books API
@router.post("/ocr", response_model=BookOCRResponse)
async def ocr_book_cover(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Extract text from image
    ocr_result = extract_book_info_from_image(file)
    title = ocr_result.get("title")
    author = ocr_result.get("author")
    raw_text = ocr_result.get("raw_text")
    metadata = None
    # Use raw_text as the query for Google Books API
    if raw_text:
        clean_query = raw_text.replace(" ", "+")
        url = f"https://www.googleapis.com/books/v1/volumes?q={clean_query}&maxResults=1"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                metadata = response.json()
        except Exception:
            metadata = None
    return BookOCRResponse(title=title, author=author, raw_text=raw_text, metadata=metadata)

# Endpoint to add a new book
# - Accepts a BookCreate payload (just a URL)
# - Fetches metadata (title, description) from the URL
# - Saves the book to the database
# - Returns the created book as a response
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(payload: BookCreate, db: Session = Depends(get_db)):
    metadata = await fetch_metadata(str(payload.url))  # Fetch title/description from the URL
    book = repo.create_book(db, payload, metadata["title"], metadata["description"])
    return book

# Endpoint to list all books in the database
# - Returns a list of BookResponse objects
@router.get("/", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return repo.get_all_books(db)

# Endpoint to get a single book by its ID
# - Returns 404 if not found
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = repo.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

# Endpoint to update a book's title/description
# - Accepts partial update (PATCH)
# - Returns 404 if not found
@router.patch("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = repo.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return repo.update_book(db, book, payload)

# Endpoint to delete a book by its ID
# - Returns 204 No Content on success
# - Returns 404 if not found
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = repo.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    repo.delete_book(db, book)
