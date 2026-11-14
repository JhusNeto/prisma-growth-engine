from fastapi import FastAPI

app = FastAPI(
    title="Prisma Growth Engine API",
    version="0.1.0",
    description="Fonte de verdade para catálogo, eventos comerciais e integrações.",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/products", tags=["products"])
def list_products() -> list[dict[str, str]]:
    """Placeholder: conecte o repositório PostgreSQL no próximo incremento."""
    return []

