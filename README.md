# cicd-with-ai

A production-ready **FastAPI** project demonstrating CI/CD integration with AI-assisted code review (GitHub Copilot), automated linting, and security scanning.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Run Locally with Docker](#run-locally-with-docker)
  - [Run Locally without Docker](#run-locally-without-docker)
- [Database Migrations](#database-migrations)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Environment Variables](#environment-variables)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.115+ |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth utilities | python-jose + passlib/bcrypt |
| Logging | structlog |
| Linting | ruff |
| Security scan | bandit |
| Testing | pytest + httpx AsyncClient |
| Containerisation | Docker (multi-stage) + docker-compose |

---

## Project Structure

```
cicd-with-ai/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py       # GET /health
│   │   │   └── items.py        # CRUD /api/v1/items
│   │   └── router.py           # APIRouter aggregator
│   ├── core/
│   │   ├── config.py           # pydantic-settings configuration
│   │   ├── database.py         # async SQLAlchemy engine + session
│   │   └── security.py         # JWT + password utilities
│   ├── models/
│   │   └── item.py             # SQLAlchemy ORM model
│   ├── schemas/
│   │   └── item.py             # Pydantic v2 request/response schemas
│   ├── services/
│   │   └── item_service.py     # CRUD business logic
│   └── main.py                 # App factory, middleware, exception handlers
├── alembic/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── conftest.py             # pytest fixtures (test DB, AsyncClient)
│   ├── test_health.py
│   └── test_items.py
├── .github/
│   ├── copilot-review-instructions.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ai-review.yml
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── .pre-commit-config.yaml
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose **or** Python 3.12+ with a running PostgreSQL instance

### Run Locally with Docker

```bash
# 1. Copy environment file
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 2. Build and start services
docker compose up --build

# 3. Apply database migrations (in a separate terminal)
docker compose exec app alembic upgrade head
```

The API will be available at **http://localhost:8000**

- Interactive docs (Swagger UI): http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Run Locally without Docker

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies (including dev extras)
pip install -e ".[dev]"

# 3. Copy and edit environment file
cp .env.example .env

# 4. Apply database migrations
alembic upgrade head

# 5. Start the development server
uvicorn app.main:app --reload
```

---

## Database Migrations

```bash
# Auto-generate a new migration from model changes
alembic revision --autogenerate -m "describe your change"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## Running Tests

Tests use an in-memory SQLite database so no external services are needed.

```bash
# Install dev dependencies (if not already done)
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

---

## CI/CD Pipeline

The `.github/workflows/ai-review.yml` workflow triggers on pull requests targeting the **`review`** branch and:

1. Runs **ruff** linting and format checks
2. Runs **bandit** security scanning
3. Automatically requests **GitHub Copilot** as a code reviewer

### Pre-commit hooks

```bash
# Install pre-commit hooks locally
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `API_ENV` | Environment name (`development` / `production`) | `development` |
| `SECRET_KEY` | Secret key for JWT signing | *(required)* |
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://...` |
| `CORS_ORIGINS` | Comma-separated allowed CORS origins | `http://localhost:3000,...` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry in minutes | `30` |

See `.env.example` for a complete template.