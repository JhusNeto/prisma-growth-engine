from pydantic import BaseModel, ConfigDict, Field


class HotmartPrice(BaseModel):
    model_config = ConfigDict(extra="ignore")

    value: float = Field(ge=0)
    currency_value: str = "BRL"


class HotmartOfferRef(BaseModel):
    model_config = ConfigDict(extra="ignore")

    code: str | None = None


class HotmartPurchase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    transaction: str = Field(min_length=1, max_length=120)
    status: str | None = None
    price: HotmartPrice
    offer: HotmartOfferRef | None = None
    approved_date: int | None = None
    order_date: int | None = None


class HotmartProductRef(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int | str | None = None
    name: str | None = None


class HotmartWebhookData(BaseModel):
    model_config = ConfigDict(extra="ignore")

    product: HotmartProductRef | None = None
    purchase: HotmartPurchase


class HotmartWebhookPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(min_length=1, max_length=160)
    creation_date: int | None = None
    event: str = Field(min_length=1, max_length=80)
    version: str | None = None
    data: HotmartWebhookData


class WebhookAck(BaseModel):
    status: str
    event_id: str
    order_id: str | None = None
    order_status: str | None = None
