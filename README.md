# Digital Book Library (Read Later API)

A FastAPI service to save and manage digital book links, with automated metadata fetching (title, description) and MySQL storage.

## Features
- Add a book by URL (auto-fetches title/description)
- List all saved books
- Get, update, or delete a book by ID
- Async metadata fetching for responsiveness
- **NEW:** Upload a book cover image and extract title/author using OCR (EasyOCR)

## Requirements
- Python 3.9+
- Docker (for MySQL)
- EasyOCR & Pillow (for OCR)
  - Install with: `pip install easyocr Pillow`
  - System dependencies may be required for OCR (e.g., `libglib2.0-0`, `libsm6`, `libxrender1`, `libxext6`)

## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd digital-book-library
```


### 2. Set up environment variables
- Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
- Edit `.env` and adjust credentials if needed:
  - `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `DATABASE_URL`

### 3. Set up the database
- Start MySQL with Docker Compose:
```bash
docker compose up -d
```


### 4. Install dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Start the FastAPI app
```bash
uvicorn app.main:app --reload
```

- The API will be available at: http://localhost:8000
- Interactive docs: http://localhost:8000/docs


## API Endpoints
- `POST   /api/v1/books`      — Add a book by URL
- `GET    /api/v1/books`      — List all books
- `GET    /api/v1/books/{id}` — Get book details
- `PATCH  /api/v1/books/{id}` — Update book title/description
- `DELETE /api/v1/books/{id}` — Delete a book
- `POST   /api/v1/books/ocr`  — **Upload a book cover image, extract title/author with OCR, and fetch metadata**



## Notes
- Tables are auto-created on app startup (no migrations needed for simple use).
- For production, consider using Alembic for migrations and secure your `.env` file. Never commit `.env` with secrets—use `.env.example` for sharing config templates.
- For OCR, see [EasyOCR documentation](https://github.com/JaidedAI/EasyOCR) if you encounter system dependency issues.

---

Happy reading!
