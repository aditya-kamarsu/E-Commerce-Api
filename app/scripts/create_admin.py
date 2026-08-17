
from app.core.database import SessionLocal
from app.modules.user.models import User
from app.core.enums import UserRole
from app.modules.auth.hashing import hash_password

from app.modules.addresses.models import Address
from app.modules.products.models import Product
from app.modules.categories.models import Category
from app.modules.cart.models import Cart
from app.modules.orders.models import Order, OrderItem
from app.modules.seller_application.models import SellerApplication



def create_admin():
    db = SessionLocal()

    try:
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            phone_number="9999999999",
            password_hash=hash_password("Admin@123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(f"Admin created: {admin.email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()