

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.authorization import require_role
from app.core.dependencies import get_db
from app.core.enums import UserRole
from app.modules.categories.dependencies import get_category_service
from app.modules.categories.schemas import (
    CreateCategory,
    UpdateCategory,
    CategoryResponse,
)
from app.modules.categories.service import CategoryService
from app.modules.user.models import User


category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@category_router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CreateCategory,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    category_service: CategoryService = Depends(
        get_category_service
    ),
):
    return category_service.create_category(
        db=db,
        category_data=category_data,
    )


@category_router.get(
    "/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_categories(
    db: Session = Depends(get_db),
    category_service: CategoryService = Depends(
        get_category_service
    ),
):
    return category_service.get_all_categories(
        db=db
    )


@category_router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    category_service: CategoryService = Depends(
        get_category_service
    ),
):
    return category_service.get_category_by_id(
        db=db,
        category_id=category_id,
    )


@category_router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
def update_category(
    category_id: int,
    category_update: UpdateCategory,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    category_service: CategoryService = Depends(
        get_category_service
    ),
):
    return category_service.update_category(
        db=db,
        category_id=category_id,
        category_update=category_update,
    )


@category_router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    category_service: CategoryService = Depends(
        get_category_service
    ),
):
    return category_service.delete_category(
        db=db,
        category_id=category_id,
    )