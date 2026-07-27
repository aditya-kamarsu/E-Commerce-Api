from sqlalchemy import select
from app.modules.orders.models import Order, OrderItem



class OrderRepository:

    def create_order(self, db, order: Order):

        try:
            db.add(order)
            db.flush()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise e 
        



    def get_by_id(self, db, order_id):
        stmt = select(Order).where(Order.id == order_id)
        return db.scalar(stmt)

    def get_by_user(self, db, user_id):
        stmt = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
        return db.scalars(stmt).all()


    def update(self, db, order):
        try:
            db.flush()
            db.refresh(order)
            return order
        except Exception:
            db.rollback()
            raise

    def delete(self, db, order):
        try:
            db.delete(order)
            db.flush()
        except Exception as e:
            db.rollback()
            raise e


class OrderItemRepository:

    def create(self, db, order_item):
        try:
            db.add(order_item)
            db.flush()
            db.refresh(order_item)
            return order_item
        except Exception:
            db.rollback()
            raise 

    def create_many(self, db, order_items):
        try:
            db.add_all(order_items)
            db.flush()
            for item in order_items:
                db.refresh(item)
            return order_items
        except Exception:
            db.rollback()
            raise 

    def get_by_order(self, db, order_id):
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        return db.scalars(stmt).all()
    

    def delete_by_order(self, db, order_id):
        try:
            stmt = select(OrderItem).where(OrderItem.order_id == order_id)
            order_items = db.scalars(stmt).all()
            for item in order_items:
                db.delete(item)
            db.flush()
        except Exception as e:
            db.rollback()
            raise e