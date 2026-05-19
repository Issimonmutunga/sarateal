from datetime import date

from pydantic import BaseModel, ConfigDict


class BuyerDemandBase(BaseModel):
    buyer_id: int
    product_id: int

    quantity_needed: float
    unit: str

    needed_from: date
    needed_until: date | None = None

    county: str
    sub_county: str | None = None
    ward: str | None = None

    target_price_per_unit: float | None = None
    requirements: str | None = None

    status: str = "open"


class BuyerDemandCreate(BuyerDemandBase):
    pass


class BuyerDemandRead(BuyerDemandBase):
    id: int

    model_config = ConfigDict(from_attributes=True)