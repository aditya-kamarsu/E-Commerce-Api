from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class WishlistProductResponse(BaseModel):
    id: int
    name: str
    description: str
    brand: str
    price: Decimal
    stock: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    created_at: datetime
    product: WishlistProductResponse

    model_config = ConfigDict(from_attributes=True)


class WishlistResponse(BaseModel):
    items: list[WishlistItemResponse]