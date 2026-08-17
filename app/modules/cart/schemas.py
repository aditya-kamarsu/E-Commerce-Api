

from decimal import Decimal

from pydantic import BaseModel, Field


class AddToCartRequestSchema(BaseModel):
    product_id: int
    quantity: int = 1


class UpdateCartItemRequestSchema(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponseSchema(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Decimal
    quantity: int
    subtotal: Decimal

class CartResponseSchema(BaseModel):
    items: list[CartItemResponseSchema]
    total: Decimal


class UpdateCartItemRequestSchema(BaseModel):
    quantity: int = Field(..., gt=0)