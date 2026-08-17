from datetime import datetime


from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column,  relationship

from app.core.database import Base
from app.modules.user.models import User



class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    # //home office parents this are the type of adress
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
        # person name for address like home address office address etc
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    address_line1: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    address_line2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    postal_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        default="India",
        nullable=False
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="addresses"
    )

    orders :Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="address",
        cascade="all, delete-orphan"
    )