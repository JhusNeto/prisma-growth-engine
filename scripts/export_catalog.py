import json
import os
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from sqlalchemy import select
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))

from app.db import get_engine
from app.models import Offer, Product
from app.page_models import ProductPage

DATA_DIR = ROOT / "apps/web/src/data"


def valid_offer(offer: Offer) -> bool:
    if not offer.active or offer.price_cents <= 0:
        return False

    try:
        url = urlsplit(offer.checkout_url or "")
        return (
            url.scheme == "https"
            and bool(url.hostname)
            and url.username is None
            and url.password is None
        )
    except ValueError:
        return False


def serialize_page(page: ProductPage | None) -> dict | None:
    if page is None:
        return None

    return {
        "headline": page.headline,
        "subheadline": page.subheadline,
        "description": page.description,
        "benefits": page.benefits,
        "faqs": page.faqs,
        "cta_label": page.cta_label,
        "seo_title": page.seo_title,
        "seo_description": page.seo_description,
    }


def serialize_product(
    product: Product,
    page: ProductPage | None,
    offers: list[Offer],
) -> dict:
    return {
        "slug": product.slug,
        "name": product.name,
        "audience": product.audience,
        "status": product.status,
        "page": serialize_page(page),
        "offers": [
            {
                "price_cents": offer.price_cents,
                "currency": offer.currency,
                "checkout_url": offer.checkout_url,
            }
            for offer in offers
        ],
    }


def build_catalog(session: Session) -> tuple[list, list]:
    products = session.scalars(select(Product).order_by(Product.slug)).all()

    public = []
    preview = []

    for product in products:
        page = session.get(ProductPage, product.id)

        offers = session.scalars(
            select(Offer).where(Offer.product_id == product.id)
        ).all()

        valid_offers = sorted(
            [offer for offer in offers if valid_offer(offer)],
            key=lambda offer: offer.price_cents,
        )

        if product.slug == "precifica-facil":
            preview.append(serialize_product(product, page, valid_offers))

        if product.status != "live":
            continue

        if page is None or not page.approved:
            raise RuntimeError(f"Produto live sem conteúdo aprovado: {product.slug}")

        if not valid_offers:
            raise RuntimeError(f"Produto live sem checkout válido: {product.slug}")

        public.append(serialize_product(product, page, valid_offers))

    return public, preview


def write_json(name: str, records: list) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    destination = DATA_DIR / name

    content = json.dumps(records, ensure_ascii=False, indent=2) + "\n"

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=DATA_DIR,
        prefix=f".{name}.",
        delete=False,
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)

    try:
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)

    print(f"{name}: {len(records)} produto(s)")


def main() -> None:
    with Session(get_engine()) as session:
        public, preview = build_catalog(session)

    # Escrever somente após validar todos os produtos live.
    write_json("catalog.public.json", public)
    write_json("catalog.preview.json", preview)


if __name__ == "__main__":
    main()
