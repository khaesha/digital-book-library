# Import SQLAlchemy Session for DB operations
from sqlalchemy.orm import Session

# Import the Book ORM model
from app.models.book import Book

# Import Pydantic schemas for type hints
from app.schemas.book import BookCreate, BookUpdate


# Create a new book record in the database
# - data: BookCreate schema (user input)
# - title, description: fetched metadata
def create_book(
    db: Session, data: BookCreate, title: str | None, description: str | None
) -> Book:
    book = Book(
        url=str(data.url), title=title, description=description
    )  # Create Book instance
    db.add(book)  # Add to session
    db.commit()  # Commit transaction (save to DB)
    db.refresh(book)  # Refresh instance with DB-generated fields (like id)
    return book


# Get all books, ordered by newest first
def get_all_books(db: Session) -> list[Book]:
    return db.query(Book).order_by(Book.created_at.desc()).all()


# Get a single book by its ID (or None if not found)
def get_book_by_id(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


# Update a book's fields (title/description)
# - Only updates fields provided in the BookUpdate schema
def update_book(db: Session, book: Book, data: BookUpdate) -> Book:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)  # Set new value for each field
    db.commit()  # Save changes
    db.refresh(book)  # Refresh instance
    return book


# Delete a book from the database
def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
