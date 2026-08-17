from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.modules.user.models import User
from app.core.database import Base
from app.modules.seller_application.utils import SellerApplicationStatus


class SellerApplication(Base):
    __tablename__ = "seller_applications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True
    )

    business_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    status: Mapped[SellerApplicationStatus] = mapped_column(
        Enum(SellerApplicationStatus),
        default=SellerApplicationStatus.PENDING,
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
        back_populates="seller_application"
    )