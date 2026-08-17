from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from app.modules.orders.utils import OrderStatus



class OrderAddressResponse(BaseModel):
    id: int
    type: str
    name: str
    phone_number: str
    address_line1: str
    address_line2: str | None
    city: str
    state: str
    postal_code: str
    country: str

    model_config = ConfigDict(from_attributes=True)
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)





class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_id: int

    shipping_fee: Decimal
    tax_amount: Decimal
    total_amount: Decimal

    status: OrderStatus

    created_at: datetime
    updated_at: datetime

    order_items: list[OrderItemResponse]
    address: OrderAddressResponse

    model_config = ConfigDict(from_attributes=True)








class CreateOrderRequest(BaseModel):
    address_id: int