from datetime import date

from pydantic import BaseModel, ConfigDict


class FarmerSupplyBase(BaseModel):
    farmer_id: int
    product_id: int

    quantity: float
    unit: str

    available_from: date
    available_until: date | None = None

    county: str
    sub_county: str | None = None
    ward: str | None = None

    expected_price_per_unit: float | None = None
    status: str = "available"


class FarmerSupplyCreate(FarmerSupplyBase):
    pass


class FarmerSupplyRead(FarmerSupplyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)