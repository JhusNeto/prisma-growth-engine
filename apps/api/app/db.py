from collections.abc import Iterator
from functools import lru_cache

from app.config import get_settings
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


@lru_cache
def get_engine() -> Engine:
    return create_engine(
        get_settings().database_url,
        pool_pre_ping=True,
    )


def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session
