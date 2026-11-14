# Prisma Growth Engine — Engineering Rules

## Mission
Build a reusable, low-cost automation platform
for distributing and selling digital microproducts.

## Architecture
- Modular monolith
- FastAPI is the business source of truth
- PostgreSQL stores transactional state
- n8n orchestrates workflows
- Astro powers public storefronts
- External checkouts process payments
- Python handles AI and background jobs

## Engineering Rules
1. Read docs/architecture/n1-n2.md before changes.
2. Respect existing ADRs.
3. Do not create microservices without an ADR.
4. Keep business logic outside n8n.
5. Use migrations for database changes.
6. All external events must be idempotent.
7. Validate and authenticate payment webhooks.
8. Never expose credentials or private assets.
9. Add tests for business logic.
10. Update documentation alongside code changes.

## Product Rules
- No unsolicited bulk prospecting.
- No misleading commercial claims.
- No fake reviews or fabricated evidence.
- Human approval for initial publications.
- Human approval for price changes.
- Respect LGPD and platform policies.

## Development
- macOS Apple Silicon
- Python 3.12
- FastAPI
- PostgreSQL 16
- Astro
- Docker Compose
- npm
- n8n

## Definition of Done
A feature is complete only when:
- Implementation works
- Automated tests pass
- Documentation is updated
- Errors are handled
- Security implications are reviewed
