# Prisma Growth Engine — Arquitetura N3

Version: 0.3.0
Status: DRAFT
Architecture: Modular Monolith
Environment: macOS Apple Silicon
Updated: 2026-11-14

## 1. Objective

Implement a reusable platform for automated distribution,
marketing, sales, fulfillment and optimization of digital
microproducts.

The system must minimize manual intervention without
assuming that automation guarantees sales or revenue.

## 2. Architecture Principles

1. FastAPI owns business rules.
2. PostgreSQL is the transactional source of truth.
3. n8n orchestrates workflows.
4. Astro renders public storefronts.
5. Python executes intelligence and background jobs.
6. External payment providers process payments.
7. Initial product publication requires approval.
8. Financial events must be authenticated and idempotent.
9. Components must remain replaceable.
10. Local execution must not require paid services.

## 3. Runtime Components

### Backend

Location: apps/api/

Technology:
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- psycopg

Responsibilities:
- Product management
- Offers
- Campaign management
- Order management
- Event processing
- Business rules
- Analytics endpoints

### Frontend

Location: apps/web/

Technology:
- Astro
- TypeScript
- CSS

Responsibilities:
- Public storefront
- Landing pages
- Product presentation
- Checkout redirection
- Tracking events

### Database

Technology: PostgreSQL 16

Responsibilities:
- Transactional persistence
- Event persistence
- Job state
- Audit records
- Idempotency controls

### Orchestration

Technology: n8n

Responsibilities:
- Workflow scheduling
- Trigger handling
- External integrations
- Content generation orchestration
- Operational notifications

Business logic must not be duplicated in n8n.

## 4. Logical Modules

### Product Core

Entities:
- Product
- Offer
- Asset
- ProductVersion

### Market Intelligence

Entities:
- ResearchTask
- MarketOpportunity
- KeywordHypothesis

### Content Factory

Entities:
- ContentItem
- ContentVersion
- Approval

### Distribution Engine

Entities:
- Campaign
- Channel
- Publication

### Conversion Engine

Entities:
- TrackingEvent
- Attribution
- CheckoutSession

### Commerce

Entities:
- Order
- PaymentProviderEvent
- Fulfillment

### Growth Intelligence

Entities:
- PerformanceSnapshot
- Experiment
- Recommendation

Entities are logical boundaries.
Physical database schemas must be reconciled with
the existing infra/postgres/init/001-schema.sql.

## 5. Product Lifecycle

DRAFT
  -> PREPARED
  -> APPROVED
  -> LIVE
  -> PAUSED
  -> ARCHIVED

Publication requires:
- Valid product data
- Approved content
- Valid checkout URL
- Configured delivery
- Successful pre-publication checks

## 6. API Design

Base path: /v1

Planned endpoints:

POST /products
GET /products
GET /products/{id}
POST /products/{id}/prepare
POST /products/{id}/approve
POST /products/{id}/publish

POST /events
POST /webhooks/hotmart

GET /analytics/overview
GET /products/{id}/performance

These routes are planned contracts, not a claim
that they are currently implemented.

## 7. Internal Event Contract

Required fields:
- event_id
- event_type
- schema_version
- source
- occurred_at
- aggregate_id
- payload

Example event types:
- product.created
- product.prepared
- product.published
- content.published
- checkout.clicked
- order.approved
- order.refunded
- fulfillment.completed

Event consumers must support duplicate delivery.

## 8. Transactional Reliability

Use PostgreSQL transactions for state transitions.

External events must be persisted before acknowledgement.

Use:
- Unique provider event identifiers
- Transactional outbox
- Idempotent event consumers
- Retry with bounded backoff
- Dead-letter or failed-job state
- Audit logs
- Operational alerts

Payment processing must never depend solely
on a successful n8n execution.

## 9. Workflow Catalogue

W01: Product Intake
W02: Market Intelligence
W03: Content Factory
W04: Publication
W05: Acquisition Monitoring
W06: Sale Webhook
W07: Fulfillment Reconciliation
W08: Growth Optimization

Every workflow must define:
- Trigger
- Input contract
- Output contract
- Dependencies
- Retry policy
- Error handling
- Idempotency behavior
- Monitoring

## 10. Security

- Environment variables for secrets
- No credentials in source control
- Administrative authentication
- Provider webhook verification
- HTTPS for public deployment
- Restricted database access
- Private storage for paid assets
- Personal data minimization
- Defined data retention
- Authorization before sensitive operations

## 11. Observability

Minimum measurements:
- Request failures
- Job failures
- Webhook processing latency
- Duplicate webhook events
- Order status
- Fulfillment status
- Website visits
- Checkout clicks
- Confirmed sales
- Refunds
- Revenue after identifiable fees

## 12. Development Environments

LOCAL:
- macOS ARM64
- FastAPI
- PostgreSQL Docker container
- n8n Docker container
- Astro development server

PUBLIC:
- Static storefront hosting
- Secure backend endpoint
- External checkout
- Persistent storage

The MacBook is a development environment,
not a guaranteed always-on production host.

## 13. Testing Strategy

Unit tests:
- Business rules
- State transitions
- Validation
- Idempotency

Integration tests:
- PostgreSQL
- API
- Event processing
- Webhook handling

End-to-end tests:
- Product registration
- Publication
- Checkout redirection
- Payment event simulation
- Delivery reconciliation

## 14. Implementation Order

Phase 1: Repository and documentation
Phase 2: Product Core
Phase 3: Persistence and migrations
Phase 4: Product API
Phase 5: Public storefront
Phase 6: Checkout integration
Phase 7: Orchestration workflows
Phase 8: Analytics
Phase 9: Distribution automation
Phase 10: Growth optimization

## 15. MVP Acceptance Criteria

The MVP is accepted when:

1. A product can be registered.
2. Product data persists in PostgreSQL.
3. A landing page can be generated.
4. Publication requires approval.
5. A valid checkout link is available.
6. Checkout clicks can be tracked.
7. Payment webhooks can be verified.
8. Duplicate events do not duplicate sales.
9. Fulfillment can be reconciled.
10. Financial metrics can be viewed.
11. Failures are traceable.
12. A second product reuses the same architecture.
