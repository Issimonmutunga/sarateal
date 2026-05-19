from datetime import date

from pydantic import BaseModel, ConfigDict


class TenderBase(BaseModel):
    title: str

    buyer_id: int | None = None
    product_id: int | None = None

    source_name: str
    source_url: str | None = None

    county: str | None = None
    quantity: float | None = None
    unit: str | None = None

    opening_date: date | None = None
    closing_date: date | None = None

    requirements: str | None = None
    status: str = "open"


class TenderCreate(TenderBase):
    pass


class TenderRead(TenderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)