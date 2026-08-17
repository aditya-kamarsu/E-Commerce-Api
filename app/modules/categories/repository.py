

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.modules.categories.models import Category
from app.modules.products.models import Product
from app.modules.categories.schemas import UpdateCategory



class CategoryRepository:


    def create(
            self,
            db:Session,
            category: Category
    ):
        try:
            db.add(category)
            db.flush()
            db.refresh(category)
            return category
        except Exception :
            db.rollback()
            raise


    def get_by_id(
            self,
            db: Session,
            category_id: int
    ) -> Category | None:
        stmt = (select(Category).where(Category.id == category_id))
        return db.scalar(stmt)

    def get_by_name(
            self,
            db: Session,
            name: str
    ) -> Category | None:
        stmt = (select(Category).where(Category.name == name))
        return db.scalar(stmt)


    def get_all(
            self,
            db: Session
    ) -> list[Category]:
        stmt = (select(Category))
        return db.scalars(stmt).all()


    def update(
            self,
            db: Session,
            category_id: int,
            category_update: UpdateCategory
    ) -> Category:
        try:
            category = self.get_by_id(db, category_id)
            if not category:
                return None

            
            for field, value in category_update.model_dump(exclude_unset=True).items():
                setattr(category, field, value)


            db.flush()
            db.refresh(category)
            return category
        except Exception:
            db.rollback()
            raise

    def delete(
            self,
            db: Session,
            category_id: int
    ) -> bool:
        try:
            category = self.get_by_id(db, category_id)
            if not category:
                return False

            db.delete(category)
            db.flush()
            return True
        except Exception:
            db.rollback()
            raise

    def has_products(
            self,
            db: Session,
            category_id: int
    ) -> bool:
        stmt = select(
            exists().where(
                Product.category_id == category_id
            )
        )

        return db.scalar(stmt)

    