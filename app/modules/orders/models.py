from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, func

from app.core.database import Base
from app.modules.orders.utils import OrderStatus



 
class Order(Base):
    __tablename__ = "orders"

    id:Mapped[int] = mapped_column(primary_key=True, index=True) 
    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False)   


    shipping_fee: Mapped[Decimal] = mapped_column(
    Numeric(10, 2),
    default=0
)

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0
    )



    total_amount:Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False)
    
  
    status:Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False

    )
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),
        server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False
                                                 )
    
    user:Mapped["User"] = relationship("User", back_populates="orders")

    order_items:Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    
    


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(nullable=False)

    price_at_purchase: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="order_items"
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_items"
    )

    