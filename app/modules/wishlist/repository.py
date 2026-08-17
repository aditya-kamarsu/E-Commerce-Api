

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.modules.wishlist.models import WishlistItem


class WishlistRepository:

    def create(self, db: Session, wishlist_item :WishlistItem):
        try:
            db.add(wishlist_item)
            db.flush()
            db.refresh(wishlist_item)
            return wishlist_item
        except Exception:
            db.rollback()
            raise


    def get_by_user(
        self,
        db: Session,
        user_id: int
    ) -> list[WishlistItem]:
        stmt = (
            select(WishlistItem)
            .where(WishlistItem.user_id == user_id)
            .order_by(WishlistItem.created_at.desc())
        )

        return db.scalars(stmt).all()


    def get_by_user_and_product(
            self,
            db: Session,
            user_id: int,
            product_id: int
    ):
        stmt = (
            select(WishlistItem)
            .where(
                WishlistItem.user_id == user_id,
                WishlistItem.product_id == product_id
            )
        )

        return db.scalar(stmt)



    def delete(
        self,
        db: Session,
        wishlist_item: WishlistItem
    ):
        try:
            db.delete(wishlist_item)
            db.flush()
            return True
        except Exception:
            db.rollback()
            raise


    def delete_all_by_user(
            self,
            db: Session,
            user_id: int
    ):
        try:
            stmt  = delete(WishlistItem).where(WishlistItem.user_id == user_id)

            db.execute(stmt)
            db.flush()

        except Exception:
            db.rollback()
            raise




    
       