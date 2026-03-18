# Digital Book Library (Read Later API)

A FastAPI service to save and manage digital book links, with automated metadata fetching (title, description) and MySQL storage.

## Features
- Add a book by URL (auto-fetches title/description)
- List all saved books
- Get, update, or delete a book by ID
- Async metadata fetching for responsiveness
- Upload a book cover image and extract title/author using OCR (EasyOCR)

## Requirements

- Python 3.12+
- Docker (for MySQL)
- EasyOCR & Pillow (for OCR)
  - System dependencies may be required (e.g., `libglib2.0-0`, `libsm6`, `libxrender1`, `libxext6`)
- Ruff (linting and formatting)
- pytest, pytest-cov, pytest-mock, pytest-asyncio (testing)
- pre-commit (automated lint/test on commit)

## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd digital-book-library
```

### 2. Set up environment variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and adjust credentials if needed:
- `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `DATABASE_URL`

### 3. Set up the database
Start MySQL with Docker Compose:
```bash
docker compose up -d
```

### 4. Install dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pre-commit install  # Enable git hooks for lint/test on commit
```

### 5. Start the FastAPI app
```bash
uvicorn app.main:app --reload
```

- API available at: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

---

## Linting, Formatting, and Tests

### Lint and format with Ruff
```bash
ruff check .
ruff format .
```

### Run all tests with coverage
```bash
pytest
```
Coverage is enforced at **70%** minimum (configured in `pytest.ini`).

### Test stack
| Package | Purpose |
|---|---|
| `pytest` | Test runner |
| `pytest-cov` | Coverage reporting |
| `pytest-mock` | Pytest-native mocking via `mocker` fixture |
| `pytest-asyncio` | Support for `async def` test functions (auto mode) |
| `respx` | Mock HTTPX requests (Google Books API, metadata fetches) |

### Pre-commit hooks
On every `git commit`, pre-commit will automatically:
- Run Ruff for linting and formatting
- Run all unit tests via pytest

To run all hooks manually:
```bash
pre-commit run --all-files
```

> **Note:** If you see `Executable pytest not found` during commit, make sure your virtualenv is activated before committing.

---

## API Endpoints
| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/books` | Add a book by URL |
| `GET` | `/api/v1/books` | List all saved books |
| `GET` | `/api/v1/books/{id}` | Get a book by ID |
| `PATCH` | `/api/v1/books/{id}` | Update title/description |
| `DELETE` | `/api/v1/books/{id}` | Delete a book |
| `POST` | `/api/v1/books/ocr` | Upload a book cover image, extract title/author with OCR |
| `GET` | `/api/v1/healthcheck` | Check service uptime |

---

## Notes
- Tables are auto-created on app startup (no migrations needed for simple use).
- For production, consider using Alembic for migrations and secure your `.env` file. Never commit `.env` with secrets — use `.env.example` for sharing config templates.
- For OCR, see [EasyOCR documentation](https://github.com/JaidedAI/EasyOCR) if you encounter system dependency issues.

---

Happy reading!

