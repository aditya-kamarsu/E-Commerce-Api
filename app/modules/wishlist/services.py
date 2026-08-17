


from sqlalchemy.orm import Session

from app.modules.wishlist.models import WishlistItem
from app.modules.wishlist.repository import WishlistRepository
from app.modules.products.repository import ProductRepository
from app.modules.user.models import User

from app.modules.products.exceptions import ProductNotFoundException
from app.modules.wishlist.exceptions import (
    ProductAlreadyInWishlistException,
    WishlistItemNotFoundException,
)


class WishlistService:

    def __init__(
        self,
        wishlist_repository: WishlistRepository,
        product_repository: ProductRepository,
    ):
        self.wishlist_repository = wishlist_repository
        self.product_repository = product_repository

    def add_to_wishlist(
        self,
        db: Session,
        product_id: int,
        current_user: User,
    ):
        try:
            # 1. Check product exists
            product = self.product_repository.get_product_by_id(
                db=db,
                product_id=product_id,
            )

            if not product:
                raise ProductNotFoundException(
                    product_id=product_id
                )

            # 2. Check product is active
            if not product.is_active:
                raise ProductNotFoundException(
                    product_id=product_id
                )

            # 3. Check duplicate
            existing_item = (
                self.wishlist_repository.get_by_user_and_product(
                    db=db,
                    user_id=current_user.id,
                    product_id=product_id,
                )
            )

            if existing_item:
                raise ProductAlreadyInWishlistException(
                    product_id=product_id
                )

            # 4. Create wishlist item
            wishlist_item = WishlistItem(
                user_id=current_user.id,
                product_id=product_id,
            )

            wishlist_item = self.wishlist_repository.create(
                db=db,
                wishlist_item=wishlist_item,
            )

            db.commit()

            return wishlist_item

        except Exception:
            db.rollback()
            raise

    def get_wishlist(
        self,
        db: Session,
        current_user: User,
    ):
        return self.wishlist_repository.get_by_user(
            db=db,
            user_id=current_user.id,
        )

    def remove_from_wishlist(
        self,
        db: Session,
        product_id: int,
        current_user: User,
    ):
        try:
            wishlist_item = (
                self.wishlist_repository.get_by_user_and_product(
                    db=db,
                    user_id=current_user.id,
                    product_id=product_id,
                )
            )

            if not wishlist_item:
                raise WishlistItemNotFoundException(
                    product_id=product_id
                )

            self.wishlist_repository.delete(
                db=db,
                wishlist_item=wishlist_item,
            )

            db.commit()

            return {
                "message": (
                    f"Product {product_id} "
                    "removed from wishlist."
                )
            }

        except Exception:
            db.rollback()
            raise

    def clear_wishlist(
        self,
        db: Session,
        current_user: User,
    ):
        try:
            self.wishlist_repository.delete_all_by_user(
                db=db,
                user_id=current_user.id,
            )

            db.commit()

            return {
                "message": "Wishlist cleared successfully."
            }

        except Exception:
            db.rollback()
            raise