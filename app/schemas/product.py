from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    category: str
    unit: str
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)