from app.routers.lifecycle import router as lifecycle_router
from app.routers.offers import router as offers_router
from app.routers.products import router as products_router
from fastapi import FastAPI

app = FastAPI(
    title="Prisma Growth Engine API",
    version="0.2.0",
    description=("Fonte de verdade para catálogo, eventos comerciais e integrações."),
)

app.include_router(products_router)
app.include_router(offers_router)
app.include_router(lifecycle_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
