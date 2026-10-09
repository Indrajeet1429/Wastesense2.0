# WASTESENSE: Database Design and Implementation

## 1. Overview

This document describes the database design and implementation completed as part of Member 2's responsibilities for the WASTESENSE project.

The objective of this contribution was to establish a reliable PostgreSQL database schema for storing machine information, workloads, resource measurements, waste detection events, alerts, savings estimates, replay results, and recommendations.

The implementation includes SQLAlchemy ORM models, relational constraints, foreign keys, indexes, Alembic migrations, seed data, and database integration tests.

## 2. Technology Stack

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| Python        | Database implementation and scripting     |
| PostgreSQL    | Relational database management            |
| SQLAlchemy    | ORM and database model definitions        |
| Alembic       | Database schema versioning and migrations |
| psycopg       | PostgreSQL connectivity                   |
| Pytest        | Automated database testing                |
| python-dotenv | Environment variable configuration        |

## 3. Database Design

The database consists of eight primary tables.

| Table                   | Purpose                                              |
| ----------------------- | ---------------------------------------------------- |
| `machines`              | Stores information about machines being monitored    |
| `workloads`             | Stores workload information associated with machines |
| `resource_measurements` | Stores resource utilization measurements             |
| `waste_events`          | Stores detected resource waste events                |
| `alerts`                | Stores alerts associated with waste events           |
| `savings`               | Stores estimated resource and cost savings           |
| `replay_results`        | Stores replay evaluation results                     |
| `recommendations`       | Stores resource optimization recommendations         |

The schema uses relational relationships to maintain consistency between related records.

### 3.1 Machines

The machines table stores information about the computing resources monitored by WASTESENSE.

It serves as a reference entity for workloads and related monitoring data.

### 3.2 Workloads

The workloads table stores workload information and its relationship to the associated machine.

Foreign-key constraints help maintain the relationship between workloads and machines.

### 3.3 Resource Measurements

The resource measurements table stores measurements used to represent resource utilization.

These records provide the underlying data required for subsequent waste detection and analysis.

### 3.4 Waste Events

The waste events table stores information about detected resource waste.

Important fields include:

* `waste_id`
* `machine_id`
* `workload_id`
* `timestamp`
* `waste_score`
* `severity`
* `waste_type`
* `confidence`
* `persistent`

The waste score is constrained to the range of 0 to 100, and confidence is constrained to the range of 0 to 1.

The severity field represents the classification of a waste event, using the supported values defined by the database model.

### 3.5 Alerts

The alerts table stores notifications associated with waste events.

It supports alert statuses such as:

* `open`
* `acknowledged`
* `resolved`

The schema also includes timestamps for alert creation and resolution.

### 3.6 Savings

The savings table stores estimated resource and cost savings associated with waste events.

It includes fields for CPU savings, memory savings, power savings, and estimated cost savings.

A unique constraint prevents multiple savings records from being associated with the same waste event.

### 3.7 Replay Results

The replay results table stores the results of replay-based evaluation.

It includes actual and expected CPU and power values, along with estimated savings.

A unique constraint prevents multiple replay result records from being associated with the same waste event.

### 3.8 Recommendations

The recommendations table stores suggested resource optimization actions associated with waste events.

It includes the recommendation text, resource type, current value, suggested value, and estimated benefit.

## 4. Database Relationships and Integrity

The schema uses foreign keys and relational constraints to preserve data integrity.

The main relationships connect:

* Machines with workloads
* Machines and workloads with resource measurements
* Machines and workloads with waste events
* Waste events with alerts
* Waste events with savings
* Waste events with replay results
* Waste events with recommendations

The database also uses constraints and indexes to support data validity and common query operations.

The exact relationship cardinalities and constraint definitions are maintained in the SQLAlchemy models and migration files.

## 5. SQLAlchemy ORM Implementation

SQLAlchemy models define the database entities and their corresponding table structures.

The ORM layer supports:

* Table and column definitions
* Primary keys
* Foreign-key relationships
* Data types and numeric precision
* Uniqueness constraints
* Check constraints
* Indexes
* Relationships between entities

Centralized database configuration allows the models and application components to use a consistent database connection configuration.

## 6. Alembic Migrations

Alembic is used to manage database schema changes.

The migration system allows the database schema to be versioned and updated in a controlled manner.

### Check the current migration

From the project root, run:

```powershell
.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini current
```

### Apply migrations

```powershell
.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini upgrade head
```

### View migration history

```powershell
.\.venv\Scripts\python.exe -m alembic -c database\alembic.ini history
```

The initial schema migration was created and applied during Day 1.

## 7. Database Configuration

The application uses environment variables to configure the PostgreSQL connection.

The following variables are used in the project configuration:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres@localhost:5432/wastesense
DATABASE_PASSWORD=your_postgres_password
```

Replace the placeholder password with the password configured for your local PostgreSQL instance.

The database connection is configured through the project's database configuration module.

**Security note:** The actual `.env` file must remain untracked. Only placeholder configuration should be committed to the repository.

## 8. Seed and Demo Data

A seed script is provided at:

`database/seeds/seed_demo.py`

The purpose of the seed data is to populate the database with demonstration records for development and testing.

Seed data helps developers verify relationships between entities and exercise database-backed functionality without manually creating every record.

Before running the seed script, ensure that PostgreSQL is running, environment variables are configured, and the database migrations have been applied.

## 9. Database Integration Tests

Database integration tests are located at:

`tests/test_database_integration.py`

The tests verify database behavior and the correctness of the schema implementation.

The database testing scope includes the database connection, table availability, and relevant database integration behavior implemented in the test suite.

Run the test suite from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_database_integration.py -v
```

To run all project tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## 10. Project Structure

The main database implementation files are organized as follows:

```text
WASTESENSE/
|
|-- database/
|   |-- models/
|   |-- migrations/
|   |-- seeds/
|   |   |-- seed_demo.py
|   |-- base.py
|   |-- session.py
|   |-- alembic.ini
|   |-- README.md
|
|-- tests/
|   |-- test_database_integration.py
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
```

The database models define the schema, Alembic manages schema migrations, the seed script provides demonstration data, and the integration tests verify database behavior.

## 11. Member 2 Deliverables

The following deliverables were completed as part of Day 1:

* PostgreSQL database configuration
* Eight SQLAlchemy database models
* Relationships and foreign-key constraints
* Data validation constraints and indexes
* Alembic configuration and initial migration
* Database schema migration
* Seed and demonstration data
* Database integration tests
* Database documentation

These deliverables establish the database foundation used by the FastAPI backend.

## 12. Relationship to Member 6's Work

Member 2's work establishes the database schema and persistence foundation.

Member 6's work builds on that foundation by integrating FastAPI with PostgreSQL, implementing database-backed API endpoints, managing request-scoped database sessions, validating API requests, and testing backend/database interactions.

The responsibilities are complementary, with the database implementation providing the foundation for backend integration.

## 13. Git Branch and Contribution

**Feature branch:** `member2-database`

**Database implementation commit:** `bd862c4`

**Commit message:** `feat(database): implement PostgreSQL schema and migrations`

Changes for the Member 2 database contribution are maintained on the feature branch rather than being pushed directly to `main`.

## 14. Conclusion


The PostgreSQL schema, SQLAlchemy models, constraints, migrations, seed data, and database integration tests provide the foundation required for backend development and subsequent ML integration.

The database can be extended as project requirements evolve, with Alembic providing a controlled mechanism for managing schema changes.
