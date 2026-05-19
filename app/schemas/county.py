from pydantic import BaseModel, ConfigDict


class CountyBase(BaseModel):
    name: str
    code: str
    region: str | None = None


class CountyCreate(CountyBase):
    pass


class CountyRead(CountyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)