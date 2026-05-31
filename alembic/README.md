# Job Tracker API

A backend API for tracking job applications.

This project was built to cover the core pieces of a real backend workflow: authentication, database design, migrations, Dockerized development, and automated testing.

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT authentication
- Passlib + bcrypt
- Docker / Docker Compose
- Pytest

## Features

- User registration and login
- JWT-based authentication
- Current user endpoint
- Job application CRUD
- PostgreSQL with Alembic migrations
- Dockerized local setup
- Automated tests for auth and jobs

## Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Jobs
- `POST /jobs`
- `GET /jobs`
- `GET /jobs/{job_id}`
- `PATCH /jobs/{job_id}`
- `DELETE /jobs/{job_id}`

### Utility
- `GET /health`

## Run with Docker

Start the app:

```bash
docker compose up --build
```

Swagger docs:

```text
http://localhost:8000/docs
```

Stop containers:

```bash
docker compose down
```

## Database Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migrations:

```bash
alembic upgrade head
```

## Running Tests

Auth tests:

```bash
PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_auth.py -v
```

Jobs tests:

```bash
PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_jobs.py -v
```

Run all tests:

```bash
PYTHONPATH=. ./.venv/bin/python -m pytest -v
```

## Example Job Payload

```json
{
  "company": "Google",
  "role": "Backend Engineer",
  "link": "https://example.com/job",
  "status": "applied",
  "notes": "first test"
}
```

## Notes

- Inside Docker, PostgreSQL is available through the `db` service name.
- Local tests use SQLite in-memory.
- Protected endpoints require authentication.
- Swagger can be used to test the full auth flow and jobs CRUD manually.

## Current Status

Implemented:
- auth flow
- jobs CRUD
- database migrations
- Docker setup
- manual Swagger testing
- auth tests
- jobs tests

Planned next:
- GitHub Actions CI
- more edge-case tests
- final project polish
