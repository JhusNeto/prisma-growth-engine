# ADR-004 — Versioned Database Migrations

Status: Accepted
Date: 2026-11-14

## Context

The Prisma Growth Engine originally initialized
PostgreSQL through Docker entrypoint SQL scripts.

This approach does not support safe incremental
schema evolution on an existing database.

## Decision

Use Alembic as the database migration mechanism.

The initial revision reproduces the existing
five-table PostgreSQL schema.

For databases created before Alembic adoption,
the baseline must be validated against a
disposable database before using alembic stamp.

## Rules

1. Never recreate the production database to migrate it.
2. Every schema change requires a versioned migration.
3. Migrations must be tested on disposable databases.
4. Existing data must be preserved.
5. Destructive changes require explicit review.
6. Never use autogenerate without reviewing the diff.
7. Keep migration documentation synchronized.
8. Maintain a tested backup and recovery procedure.

## Consequences

- Reproducible database creation
- Explicit schema history
- Additional migration review responsibility
- Initial Docker SQL remains legacy bootstrap code

## Future Work

Remove duplicate schema initialization responsibilities
after the Alembic-based bootstrap is fully implemented.
