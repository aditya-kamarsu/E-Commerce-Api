
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict,Field


class CreateProduct(BaseModel):
    name: str
    description: str
    brand: str | None
    price: Decimal  = Field(gt=0, description="Price must be greater than zero")
    stock: int = Field(ge=0, description="Stock must be greater than or equal to zero")
    category_id: int 



class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    brand: str | None = None
    price: Decimal | None = None
    stock: int | None = None
    category_id: int | None = None

class ProductResponse(BaseModel):
    id: int
    seller_id: int
    category_id: int
    name: str
    description: str
    brand: str | None
    price: Decimal
    stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    
    model_config = ConfigDict(from_attributes=True)






class ProductQueryParams(BaseModel):
    search: str | None = None

    category_id: int | None = None
    brand: str | None = None

    min_price: Decimal | None = Field(default=None, gt=0, description="Minimum price must be greater than zero")
    max_price: Decimal | None = Field(default=None, gt=0, description="Maximum price must be greater than zero")

    sort: str | None = Field(default=None, description="Sort by field, e.g., 'price', 'name', etc.")

    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    limit: int = Field(default=10, ge=1,le=100, description="Limit for pagination")
    