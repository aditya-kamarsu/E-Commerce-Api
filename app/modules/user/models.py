from sqlalchemy import Boolean,  String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base






class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    first_name : Mapped[str] = mapped_column(String(50), nullable=True)
    last_name : Mapped[str] = mapped_column(String(50), nullable=True)
    email : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number : Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    password_hash : Mapped[str] = mapped_column(String(255), nullable=False)
    profile_image_url : Mapped[str] = mapped_column(String(255), nullable=True)
    role : Mapped[str] = mapped_column(String(50), nullable =False, default="customer")
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified : Mapped[bool] = mapped_column(Boolean, default=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    products: Mapped[list["Product"]] = relationship("Product", 
                                                            back_populates="seller", 
                                                            cascade="all, delete-orphan"
                                                            )
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")

    orders:Mapped[list["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")   

    def __repr__(self):
        return f"<User(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')>"
    



