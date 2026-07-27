from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from app.modules.orders.utils import OrderStatus


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
    shipping_fee: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)