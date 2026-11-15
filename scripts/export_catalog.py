import json
import sys
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


def valid_offer(offer):
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


def serialize(product, offers):
    return {
        "slug": product.slug,
        "name": product.name,
        "audience": product.audience,
        "status": product.status,
        "offers": [
            {
                "price_cents": offer.price_cents,
                "currency": offer.currency,
                "checkout_url": offer.checkout_url,
            }
            for offer in offers
        ],
    }


with Session(get_engine()) as session:
    products = session.scalars(select(Product).order_by(Product.slug)).all()

    public = []
    preview = []

    for product in products:
        offers = session.scalars(
            select(Offer).where(Offer.product_id == product.id)
        ).all()

        valid_offers = sorted(
            [offer for offer in offers if valid_offer(offer)],
            key=lambda offer: offer.price_cents,
        )

        record = serialize(product, valid_offers)

        if product.slug == "precifica-facil":
            preview.append(record)

        if product.status == "live":
            page = session.get(ProductPage, product.id)

            if page is None or not page.approved:
                raise SystemExit(f"Produto live sem conteúdo aprovado: {product.slug}")

        if product.status == "live":
            if not valid_offers:
                raise SystemExit(f"Produto live sem checkout válido: {product.slug}")

            public.append(record)


def write_json(name, records):
    path = DATA_DIR / name
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    print(f"{path.name}: {len(records)} produto(s)")


write_json("catalog.preview.json", preview)
write_json("catalog.public.json", public)
