from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.config import Settings, get_settings


def require_admin(
    settings: Annotated[Settings, Depends(get_settings)],
    x_admin_key: Annotated[str | None, Header()] = None,
) -> None:
    if not x_admin_key or not compare_digest(x_admin_key, settings.admin_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid administrative key",
        )
