# Product Pages — PC-003.2B

Status: VALIDATED LOCALLY
Database revision: 0003_product_page_content

## Objective

Provide an administrative API to create, edit,
retrieve and approve structured commercial content.

## Endpoints

PUT /v1/products/{product_id}/page
GET /v1/products/{product_id}/page
POST /v1/products/{product_id}/page/approve

All endpoints require X-Admin-Key.

## Content Contract

- headline
- subheadline
- description
- benefits
- faqs
- cta_label
- seo_title
- seo_description

Benefits are a list of strings.

FAQs are objects containing question and answer.

## Approval Rules

- New content begins unapproved.
- Saving content invalidates existing approval.
- Approval is a separate administrative action.
- Approved content is required before publication.
- Published and archived content cannot be edited.
- Published products must be paused before editing.

## Events

- product.page_saved
- product.page_approved

Both events are committed transactionally
with their corresponding database changes.

Events are stored in the outbox but are not
yet dispatched.

## Export Safety

The static catalog exporter rejects live products
that lack approved commercial content.

The public Astro template does not yet render
the structured marketing content.

## Limitations

Approval confirms an administrative action,
not independent verification of commercial claims.

X-Admin-Key does not identify an individual operator.

## Next Increment

PC-003.2C:
- Render approved content in Astro
- Structured SEO metadata
- FAQ and benefits sections
- Validation of production builds
- Publication pipeline safeguards
