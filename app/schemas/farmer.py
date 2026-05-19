from pydantic import BaseModel, ConfigDict


class FarmerBase(BaseModel):
    full_name: str
    phone_number: str

    county: str
    sub_county: str | None = None
    ward: str | None = None

    farmer_group: str | None = None
    is_verified: bool = False
    is_active: bool = True


class FarmerCreate(FarmerBase):
    pass


class FarmerRead(FarmerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)