# WASTESENSE Database

PostgreSQL database for storing WASTESENSE monitoring and intelligence data.

## Database

- PostgreSQL
- Database name: `wastesense`
- Port: `5432`

## Stored Data

- Machines
- Workloads
- Resource measurements
- Waste events
- Alerts
- Savings estimates
- Replay results
- Recommendations

## Ownership

Database implementation is owned by Member 2 and Member 6.

- Member 2: Database schema and migrations
- Member 6: Backend database integration and repositories

## Rules

- Never commit database passwords or secrets.
- Use `.env` for local credentials.
- Use migrations for schema changes.
- Do not modify another member's database files without coordination.