# WASTESENSE Backend and Database

## Overview

WASTESENSE uses FastAPI for its REST API and PostgreSQL for persistent
application data. SQLAlchemy provides ORM/database access, and Alembic
manages database schema migrations.

## Prerequisites

- Python 3.12
- PostgreSQL
- Git

## Local Setup

1. Clone the repository and open its root directory.
2. Create and activate a virtual environment if one does not exist:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1

Install dependencies:

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Create your local environment file:

Copy-Item .env.example .env
Edit .env and replace the placeholder password with your local
PostgreSQL password. Never commit .env.
Ensure PostgreSQL is running and the wastesense database exists.
Environment Configuration

The application uses these environment variables:

APP_NAME: Application name.
APP_VERSION: Application version.
DATABASE_URL: SQLAlchemy PostgreSQL connection URL.
DATABASE_PASSWORD: PostgreSQL password, supplied separately.

The example URL assumes PostgreSQL is running locally on port 5432 and
the database is named wastesense. Adjust the URL for your environment.

Database Migrations

Check the current migration revision:

.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini current

Apply pending migrations:

.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini upgrade head

The Alembic configuration is located at database/alembic.ini.

Start the API

Run from the repository root:

.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload

FastAPI's interactive documentation is available at /docs on the local
server. The OpenAPI schema is available at /openapi.json.

API Route Groups

The API currently includes:

Health checks, including database health
Machines
Workloads
Resource measurements
Waste events
Alerts and alert status updates
Savings
Replay results
Recommendations

The registered API routes use the /api/v1 prefix.

Run Tests

Run the complete test suite:

.\.venv\Scripts\python.exe -m pytest -v

Check dependency consistency:

.\.venv\Scripts\python.exe -m pip check

The integration tests cover API validation, database operations, alert
status transitions, duplicate protection, filtering, and relationships.

Security Notes
Never commit .env or real database credentials.
Use placeholder values in .env.example.
Do not expose PostgreSQL publicly without appropriate security controls.
Use environment-specific credentials outside local development.
