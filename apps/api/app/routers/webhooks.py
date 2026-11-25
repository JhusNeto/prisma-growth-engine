from secrets import compare_digest
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_session
from app.services.hotmart_webhook import process_hotmart_webhook
from app.webhook_schemas import HotmartWebhookPayload, WebhookAck

router = APIRouter(
    prefix="/v1/webhooks",
    tags=["webhooks"],
)


def require_hotmart_hottok(
    settings: Annotated[Settings, Depends(get_settings)],
    x_hotmart_hottok: Annotated[str | None, Header()] = None,
) -> None:
    expected = settings.hotmart_hottok
    if not expected or not x_hotmart_hottok or not compare_digest(x_hotmart_hottok, expected):
        raise HTTPException(
            status_code=401,
            detail="Invalid Hotmart webhook token",
        )


@router.post(
    "/hotmart",
    response_model=WebhookAck,
    dependencies=[Depends(require_hotmart_hottok)],
)
def receive_hotmart_webhook(
    payload: HotmartWebhookPayload,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | None]:
    return process_hotmart_webhook(session, payload)
