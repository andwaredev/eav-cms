# EAV CMS Backend

Python FastAPI backend for the EAV CMS application.

## Setup

### 1. Install Dependencies

Using [uv](https://docs.astral.sh/uv/):

```bash
cd backend
uv sync
```

That's it! uv handles the virtual environment and dependencies automatically.

### 2. Start PostgreSQL

From the project root (requires Docker):

```bash
docker compose up -d
```

This starts PostgreSQL 17 on port 5432 with:
- Database: `eav_cms`
- User: `eav_user`
- Password: `eav_password`

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if you need to customize the database connection.

### 4. Run Migrations

```bash
uv run yoyo apply
```

This creates the EAV schema and seeds initial data.

## Running the Server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

Run tests:
```bash
uv run pytest
```

Add a dependency:
```bash
uv add <package-name>
```

## Database Migrations

Migrations use [yoyo-migrations](https://ollycope.com/software/yoyo/latest/) with plain SQL.

```bash
uv run yoyo apply      # Apply pending migrations
uv run yoyo rollback   # Rollback last migration
uv run yoyo list       # Show migration status
```

Create a new migration in `migrations/` following the naming convention `NNNN_description.py`.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   └── routers/         # API route handlers
│       ├── __init__.py
│       └── health.py    # Health check endpoints
├── migrations/          # Database migrations (yoyo)
│   ├── 0001_create_eav_tables.py
│   └── 0002_seed_data.py
├── tests/               # Unit tests
│   ├── conftest.py      # Shared test fixtures
│   ├── test_main.py
│   └── test_health.py
├── pyproject.toml       # Project config and dependencies
├── yoyo.ini             # Migration configuration
├── .env.example         # Environment template
└── README.md
```
