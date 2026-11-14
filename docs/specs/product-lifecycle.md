# Product Lifecycle — PC-002.4

Status: VALIDATED LOCALLY
Database revision: 0002_product_lifecycle

## Objective

Manage the lifecycle of digital products through
explicit state transitions and commercial safeguards.

## Endpoint

POST /v1/products/{product_id}/transitions

Authentication: X-Admin-Key

## Allowed Transitions

- draft -> prepared, archived
- prepared -> draft, approved, archived
- approved -> prepared, live, archived
- live -> paused
- paused -> live, archived
- archived -> terminal

## Publication Requirements

Publishing or republishing requires:

1. An allowed state transition
2. At least one active offer
3. A positive offer price
4. An HTTPS checkout URL
5. Administrator confirmation of checkout testing
6. Administrator confirmation of delivery testing
7. Explicit publication approval

Manual confirmations are attestations, not
independent validation of payment or delivery.

## Commercial Safeguards

Offers cannot be created or modified while
the product is live.

The product must be paused first.

## Audit

Each successful transition persists a
product.status_changed event in the outbox.

The event records:
- Product ID
- Previous status
- New status
- Reason
- Authentication method
- Publication confirmations when applicable

## Deferred

- Named administrator identities
- Independent checkout verification
- Automatic delivery verification
- Event outbox dispatch
- Public storefront
- Payment provider integration
