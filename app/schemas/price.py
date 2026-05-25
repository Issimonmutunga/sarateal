from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class PriceBase(BaseModel):
    product_id: int
    market_id: int | None = None

    county: str
    unit: str

    price: float
    currency: str = "KES"

    observed_on: date
    source_name: str
    source_url: str | None = None

    confidence_score: float = 1.0
    notes: str | None = None


class PriceCreate(PriceBase):
    pass


class PriceRead(PriceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)