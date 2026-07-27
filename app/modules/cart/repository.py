



from sqlalchemy.orm import Session, selectinload
from sqlalchemy import delete, select

from app.modules.cart.models import Cart, CartItem


class CartRepository:

    def get_by_user_id(self,db: Session, user_id: int):
        stmt = select(Cart).where(Cart.user_id == user_id)
        return db.scalar(stmt)

    def create_cart(self,db: Session,cart: Cart):
        try:
            db.add(cart)
            db.commit()
            db.refresh(cart)
            return cart
        except Exception as e:
            db.rollback()
            raise e
        

        

    def delete_cart(self,db: Session, cart:Cart):
        try:
            db.delete(cart)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
       



class CartItemRepository:

    def get_by_cart_and_product(self,db: Session, cart_id: int, product_id: int):
        stmt = select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        return db.scalar(stmt)


    def get_all_by_cart(self,db: Session, cart_id: int):
            stmt = select(CartItem).options(selectinload(CartItem.product)).where(CartItem.cart_id == cart_id)
            return db.scalars(stmt).all()
    

    def create_cart_item(self,db: Session, cartitem: CartItem):
        try:
            db.add(cartitem)
            db.commit()
            db.refresh(cartitem)
            return cartitem
        except Exception as e:
            db.rollback()
            raise e

    def update_cart_item(self,db: Session, cartitem: CartItem):
                """Update an existing CartItem instance in the database.

                Expected usage:
                - Modify attributes on the cartitem instance before calling this method
                    (e.g. cartitem.quantity = 3).
                - Pass the same Session that loaded or is tracking the cartitem.

                Behavior:
                - Commits the current transaction so changes on the tracked cartitem
                    are persisted to the database.
                - Refreshes the cartitem from the DB to return the latest state
                    (including any DB-side defaults or triggers).
                - On error, rolls back the transaction and re-raises the exception.
                """
                # At this point the cartitem object should already be attached to the
                # provided Session and contain the modifications to persist.
                try:
                        # Persist changes made to the tracked cartitem
                        db.commit()
                        # Reload fields from the DB to reflect any changes made by the DB
                        db.refresh(cartitem)
                        return cartitem
                except Exception as e:
                        # Undo the transaction on failure to keep Session in a clean state
                        db.rollback()
                        raise e

    def delete_cart_item(self,db: Session, cartitem: CartItem):
        try:
            db.delete(cartitem)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        
    def delete_all_by_cart(self,
                           db: Session, cart_id: int):
        try:
            stmt = delete(CartItem).where(CartItem.cart_id == cart_id)
            db.execute(stmt)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
    
    def get_cart_item_by_id(self, db: Session, cart_item_id: int):
        stmt = select(CartItem).where(CartItem.id == cart_item_id)
        return db.scalar(stmt)

    