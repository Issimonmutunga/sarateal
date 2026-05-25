from pydantic import BaseModel, ConfigDict


class MarketBase(BaseModel):
    name: str
    county: str

    sub_county: str | None = None
    ward: str | None = None

    market_type: str = "general"
    description: str | None = None

    is_active: bool = True


class MarketCreate(MarketBase):
    pass


class MarketRead(MarketBase):
    id: int

    model_config = ConfigDict(from_attributes=True)