import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.analytics import router as analytics_router
from app.routers.lifecycle import router as lifecycle_router
from app.routers.offers import router as offers_router
from app.routers.outbox import router as outbox_router
from app.routers.pages import router as pages_router
from app.routers.products import router as products_router
from app.routers.tracking import router as tracking_router
from app.routers.webhooks import router as webhooks_router

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.sentry_environment,
        send_default_pii=False,
    )

app = FastAPI(
    title="Prisma Growth Engine API",
    version="0.5.0",
    description=("Fonte de verdade para catálogo, eventos comerciais e integrações."),
)
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in settings.cors_origins.split(",")
            if origin.strip()
        ],
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

app.include_router(products_router)
app.include_router(offers_router)
app.include_router(lifecycle_router)
app.include_router(pages_router)
app.include_router(webhooks_router)
app.include_router(outbox_router)
app.include_router(analytics_router)
app.include_router(tracking_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
