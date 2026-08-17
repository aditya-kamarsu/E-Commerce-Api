




from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.products.models import Product
from app.modules.products.schemas import ProductQueryParams, UpdateProduct
from app.modules.products.exceptions import InvalidPriceRangeException


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
        query:ProductQueryParams,) -> list[Product]:
        stmt = select(Product)

        if (query.min_price is not None and query.max_price is not None and query.min_price > query.max_price):
             raise InvalidPriceRangeException(query.min_price, query.max_price)

        if query.search:
            search = f"%{query.search}%"

            stmt = stmt.where(Product.name.ilike(search) | Product.description.ilike(search))
              
        if query.category_id is not None:
             stmt = stmt.where(
                  Product.category_id == query.category_id
                  )
        if query.brand:
             stmt = stmt.where(
                  Product.brand.ilike(f"%{query.brand}%")
             )


        if query.min_price is not None:
             stmt = stmt.where(
                  Product.price >= query.min_price
             )

        if query.max_price is not None:
                stmt = stmt.where(
                    Product.price <= query.max_price
                )
        if query.sort == "price_asc":
            stmt = stmt.order_by(Product.price.asc())

        elif query.sort == "price_desc":
            stmt = stmt.order_by(Product.price.desc())
        elif query.sort == "newest":
            stmt = stmt.order_by(Product.created_at.desc())

        elif query.sort == "oldest":
            stmt = stmt.order_by(Product.created_at.asc())

        stmt = (
             stmt
             .offset(query.offset)
             .limit(query.limit)
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