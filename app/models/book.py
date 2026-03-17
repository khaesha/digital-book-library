# Import datetime for timestamp fields
from datetime import datetime

# SQLAlchemy column types
from sqlalchemy import String, Text, DateTime

# SQLAlchemy ORM typing and column definition helpers
from sqlalchemy.orm import Mapped, mapped_column

# Import the Base class for ORM models
from app.database import Base


# Define the Book table as a Python class
class Book(Base):
    __tablename__ = "books"  # Table name in the database

    # Primary key column (auto-increment integer)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # URL of the book (string, required)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    # Title of the book (string, optional)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Description of the book (text, optional)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Timestamp when the book was added (defaults to now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
