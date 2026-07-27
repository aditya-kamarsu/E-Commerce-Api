




from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.products.models import Product
from app.modules.products.schemas import UpdateProduct


class ProductRepository:
    def create_product(
        self,
        db: Session,
        product: Product
    ) -> Product:
        try:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except Exception:
            db.rollback()
            raise



    def get_product_by_id(
                self,
                db: Session,
                product_id: int
            ) -> Product | None:
                stmt = (
                    select(Product)
                    .where(Product.id == product_id)
                )

                return db.scalar(stmt)

    


    def get_all_products(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 10
    ) -> list[Product]:
        stmt = (
            select(Product)
            .offset(offset)
            .limit(limit)
        )

        return db.scalars(stmt).all()



    def update_product(self,db: Session,product: Product) -> Product:
        try:
            db.commit()
            db.refresh(product)
            return product
        except Exception:
             db.rollback()
             raise

    def delete_product(self, db: Session, product_id: int) -> bool:
        db_product = self.get_product_by_id(db, product_id)
        if not db_product:
            return False
        try:
            db.delete(db_product)
            db.commit()
        except Exception:
            db.rollback()
            raise


    def get_by_seller_and_name(
        self,
        db: Session,
        seller_id: int,
        name: str
    ) -> Product | None:
        stmt = select(Product).where(Product.seller_id == seller_id, Product.name == name)
        return db.scalar(stmt)