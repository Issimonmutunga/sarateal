from pydantic import BaseModel, ConfigDict


class BuyerBase(BaseModel):
    name: str
    buyer_type: str

    contact_person: str | None = None
    phone_number: str | None = None
    email: str | None = None

    county: str
    sub_county: str | None = None
    ward: str | None = None

    is_verified: bool = False
    is_active: bool = True


class BuyerCreate(BuyerBase):
    pass


class BuyerRead(BuyerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)