from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text,DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)

    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    brand: Mapped[str|None] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False)    
    stock: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,default = datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default = datetime.now, onupdate = datetime.now, nullable=False)

    seller: Mapped["User"] = relationship("User", back_populates="products")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    