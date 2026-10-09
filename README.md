# WASTESENSE: Backend and Database Integration

## 1. Overview

This document describes the backend and database integration implemented for the WASTESENSE project as part of Member 6's responsibilities.

The implementation connects the FastAPI backend to PostgreSQL, provides database-backed REST API endpoints, validates incoming requests, manages database sessions, and includes automated tests for backend and database integration.

The backend provides the persistence layer required to store and retrieve machine information, workloads, resource measurements, waste detection events, alerts, savings estimates, replay results, and recommendations.

**Current status:** Backend and database integration is implemented and tested. Integration with the actual ML inference component remains pending because Member 5's implementation is not yet available.

## 2. Technology Stack

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | Backend programming language       |
| FastAPI    | REST API framework                 |
| PostgreSQL | Relational database                |
| SQLAlchemy | ORM and database operations        |
| Alembic    | Database schema migrations         |
| Pydantic   | Request validation and API schemas |
| psycopg    | PostgreSQL database connectivity   |
| Uvicorn    | ASGI development server            |
| Pytest     | Automated testing                  |
| HTTPX      | HTTP client support for API tests  |

## 3. Implemented Responsibilities

### 3.1 FastAPI and PostgreSQL Integration

The FastAPI backend connects to PostgreSQL through SQLAlchemy.

Database configuration is loaded from environment variables rather than hardcoded credentials.

The implementation includes:

* Database engine configuration
* SQLAlchemy session management
* Database dependency injection
* Database-backed API operations
* Database connection health checking
* Transaction rollback and session cleanup

### 3.2 Database Models

The database contains the following primary entities:

| Table                   | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `machines`              | Stores machine information                   |
| `workloads`             | Stores workload information                  |
| `resource_measurements` | Stores resource measurement records          |
| `waste_events`          | Stores detected waste events                 |
| `alerts`                | Stores alerts associated with waste events   |
| `savings`               | Stores estimated resource and cost savings   |
| `replay_results`        | Stores replay evaluation results             |
| `recommendations`       | Stores resource optimization recommendations |

The schema uses relationships, foreign keys, and constraints to maintain data integrity.

Unique constraints are implemented for savings and replay results associated with waste events.

### 3.3 Database Migrations

Alembic manages database schema migrations.

The current migration revision verified during development is:

`064d155dfb0a`

To check the current migration state, run:

```powershell
.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini current
```

To apply pending migrations, run:

```powershell
.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini upgrade head
```

### 3.4 Database Session Management

The backend uses a shared database session dependency for route handlers.

The session management implementation supports:

* Creating database sessions for requests
* Closing sessions after requests
* Rolling back transactions when exceptions occur
* Reusing the configured SQLAlchemy engine

### 3.5 REST API Endpoints

The backend exposes the following API routes.

| Endpoint                  | Supported operations                            |
| ------------------------- | ----------------------------------------------- |
| `/api/v1/health`          | Application health check                        |
| `/api/v1/health/database` | Database connectivity check                     |
| `/api/v1/machines`        | Create, list, retrieve, and manage machines     |
| `/api/v1/workloads`       | Create and retrieve workloads                   |
| `/api/v1/measurements`    | Create and retrieve resource measurements       |
| `/api/v1/waste-events`    | Create and retrieve waste events                |
| `/api/v1/alerts`          | Create and retrieve alerts, update alert status |
| `/api/v1/savings`         | Create and retrieve savings records             |
| `/api/v1/replay-results`  | Create and retrieve replay results              |
| `/api/v1/recommendations` | Create and retrieve recommendations             |

The machine endpoints support CRUD operations. Other resources support the operations implemented in their respective route modules.

For exact request and response schemas, use the Swagger documentation provided by FastAPI.

### 3.6 Request Validation and Error Handling

Pydantic schemas validate incoming request data before database operations.

The backend includes validation for fields such as waste scores, confidence values, severity levels, and alert statuses.

The implementation also uses database constraints to protect data integrity.

Invalid requests should receive appropriate HTTP error responses, while database exceptions must be handled without exposing credentials or sensitive configuration details.

### 3.7 Automated Testing

Automated tests cover API behavior and database integration.

The test suite includes:

* API integration tests
* Database integration tests
* Request validation
* Database-backed endpoint behavior
* Error handling and data integrity checks

The last recorded test run completed with **16 passed tests and 1 warning**.

Run the complete test suite using:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

### 3.8 API Documentation

FastAPI automatically generates interactive API documentation.

After starting the backend, open:

**Swagger UI:** `http://127.0.0.1:8000/docs`

**Application health:** `http://127.0.0.1:8000/api/v1/health`

**Database health:** `http://127.0.0.1:8000/api/v1/health/database`

These URLs are for local development.

## 4. Project Structure

The main backend and database components are organized as follows:

```text
WASTESENSE/
|
|-- backend/
|   |-- main.py
|   |-- api/
|   |   |-- routes/
|   |-- db/
|       |-- dependencies.py
|
|-- database/
|   |-- alembic.ini
|   |-- base.py
|   |-- session.py
|   |-- seeds/
|   |   |-- seed_demo.py
|
|-- tests/
|   |-- test_api_integration.py
|   |-- test_database_integration.py
|
|-- docs/
|   |-- backend-database-integration.md
|
|-- requirements.txt
|-- .env.example
|-- .gitignore
```

This structure highlights the primary files involved in backend and database integration. Other model, schema, migration, and route files may exist within their respective directories.

## 5. Local Setup

### Prerequisites

Install or configure the following:

* Python 3.12 or a compatible Python version
* PostgreSQL
* Git

### Step 1: Clone the repository

```powershell
git clone https://github.com/Indrajeet1429/WASTESENSE.git
cd WASTESENSE
```

### Step 2: Create a virtual environment

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root based on `.env.example`.

Configure the PostgreSQL connection details for your local environment.

Example configuration:

```dotenv
APP_NAME=WASTESENSE API
APP_VERSION=0.1.0

DATABASE_URL=postgresql+psycopg://postgres@localhost:5432/wastesense
DATABASE_PASSWORD=your_postgres_password
```

Replace the placeholder password with your local PostgreSQL password.

**Security:** Never commit your actual `.env` file or database password to Git.

### Step 5: Apply database migrations

```powershell
python -m alembic -c database\alembic.ini upgrade head
```

### Step 6: Start the backend

```powershell
python -m uvicorn backend.main:app --reload
```

### Step 7: Verify the application

Open the following local URLs:

* Swagger UI: `http://127.0.0.1:8000/docs`
* Application health: `http://127.0.0.1:8000/api/v1/health`
* Database health: `http://127.0.0.1:8000/api/v1/health/database`

## 6. Testing

Run the complete test suite:

```powershell
python -m pytest -v
```

Check the database migration:

```powershell
python -m alembic -c database\alembic.ini current
```

Check installed dependency compatibility:

```powershell
python -m pip check
```

## 7. ML Integration Status

The backend provides the database models and API infrastructure needed to persist waste detection results.

The intended integration flow is:

```text
Resource Measurements
          |
          v
      ML Inference
          |
          v
   Validate Prediction
          |
          v
     Waste Event
          |
          v
      PostgreSQL
          |
          v
 Alerts and Recommendations
```

The actual inference component is the responsibility of Member 5.

Until that component is available, the persistence interface can be tested with controlled mock predictions. Mock data is for integration testing only and does not represent actual model inference.

The following tasks remain dependent on the ML implementation:

* Confirming the actual prediction input and output formats
* Connecting the real inference component to the backend
* Validating actual model outputs
* Testing the complete workflow with real inference results

## 8. Production Readiness

The current implementation is designed for local development and project integration.

Before production deployment, the following should be reviewed:

* Production PostgreSQL configuration
* Secure environment-variable management
* Database backups and recovery procedures
* Connection pooling and connection limits
* Production server configuration
* Authentication and authorization requirements
* Logging and monitoring
* Deployment-specific testing

These considerations should be addressed according to the final project requirements and hosting environment.

## 9. Member 6 Deliverables

Member 6 is responsible for backend and database integration.

The implemented deliverables include:

* FastAPI and PostgreSQL integration
* Database session dependency
* Database-backed API endpoints
* Request validation through Pydantic schemas
* Database transaction and session handling
* Backend and database integration tests
* API health endpoints
* API documentation
* Database integration documentation

The remaining integration work includes connecting the actual ML inference component when Member 5's implementation becomes available and completing system-level integration tests.

## 10. Git Branch

The backend and database integration work is maintained on:

`member6-backend-db`

Changes should be committed and pushed to this feature branch. They should not be pushed directly to `main`.

---

**Status:** Backend and database integration implemented. Automated tests passing in the last recorded run. Actual ML inference integration and production deployment remain pending.
