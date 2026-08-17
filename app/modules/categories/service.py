

from sqlalchemy.orm import Session
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schemas import CreateCategory
from app.modules.categories.schemas import UpdateCategory
from app.modules.categories.models import Category
from app.modules.categories.exceptions import (
    DuplicateCategoryException,
    CategoryNotFoundException,
    CategoryHasProductsException
)

class CategoryService:

    def __init__(
        self,
        category_repository: CategoryRepository
    ):
        self.category_repository = category_repository

    def create_category(
        self,
        db: Session,
        category_data: CreateCategory
    ):
        try:
            existing_category = self.category_repository.get_by_name(
                db=db,
                name=category_data.name
            )

            if existing_category:
                raise DuplicateCategoryException(
                    category_data.name
                )

            category = Category(
                **category_data.model_dump()
            )

            category = self.category_repository.create(
                db=db,
                category=category
            )

            db.commit()

            return category

        except Exception:
            db.rollback()
            raise

    def get_category_by_id(
        self,
        db: Session,
        category_id: int
    ):
        category = self.category_repository.get_by_id(
            db=db,
            category_id=category_id
        )

        if not category:
            raise CategoryNotFoundException(
                category_id
            )

        return category

    def get_all_categories(
        self,
        db: Session
    ):
        return self.category_repository.get_all(
            db=db
        )

    def update_category(
        self,
        db: Session,
        category_id: int,
        category_update: UpdateCategory
    ):
        try:
            category = self.category_repository.get_by_id(
                db=db,
                category_id=category_id
            )

            if not category:
                raise CategoryNotFoundException(
                    category_id
                )

            # Check duplicate name only if name is being changed
            if category_update.name is not None:

                existing_category = (
                    self.category_repository.get_by_name(
                        db=db,
                        name=category_update.name
                    )
                )

                if (
                    existing_category
                    and existing_category.id != category.id
                ):
                    raise DuplicateCategoryException(
                        category_update.name
                    )

            category = self.category_repository.update(
                db=db,
                category_id=category_id,
                category_update=category_update
            )

            db.commit()

            return category

        except Exception:
            db.rollback()
            raise

    def delete_category(
        self,
        db: Session,
        category_id: int
    ):
        try:
            category = self.category_repository.get_by_id(
                db=db,
                category_id=category_id
            )

            if not category:
                raise CategoryNotFoundException(
                    category_id
                )

            if self.category_repository.has_products(
                db=db,
                category_id=category_id
            ):
                raise CategoryHasProductsException(
                    category_id
                )

            self.category_repository.delete(
                db=db,
                category_id=category_id
            )

            db.commit()

            return {
                "message": (
                    f"Category with ID {category_id} "
                    "deleted successfully."
                )
            }

        except Exception:
            db.rollback()
            raise