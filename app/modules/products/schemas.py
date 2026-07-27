
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict,Field


class CreateProduct(BaseModel):
    name: str
    description: str
    brand: str | None
    price: Decimal  = Field(gt=0, description="Price must be greater than zero")
    stock: int = Field(ge=0, description="Stock must be greater than or equal to zero")



class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    brand: str | None = None
    price: Decimal | None = None
    stock: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    brand: str | None
    price: Decimal
    stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)