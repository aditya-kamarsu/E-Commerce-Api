
from datetime import datetime,UTC



from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, ForeignKey, UniqueConstraint
class Cart(Base):
    """
    Cart model
    """
    __tablename__ = "carts"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now(UTC))


    user: Mapped["User"] = relationship("User", back_populates="cart")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    """
    CartItem model
    """
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="uq_cart_product",
        ),  
        CheckConstraint(
        "quantity > 0",
        name="ck_cart_item_quantity_positive",
    ),
    )

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cart_id:Mapped[int] = mapped_column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id:Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity:Mapped[int] = mapped_column(Integer, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now(UTC))

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")