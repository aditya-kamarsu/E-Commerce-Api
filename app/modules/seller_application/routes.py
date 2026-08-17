from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import (
    get_current_user,
)
from app.core.authorization import require_role
from app.modules.seller_application.schema import CreateSellerApplication, SellerApplicationResponse
from app.modules.seller_application.service import SellerApplicationService
from app.modules.user.models import User
from app.core.enums import UserRole
from app.modules.seller_application.dependencies import get_seller_application_service



seller_application_router = APIRouter(
    prefix="/seller-applications",
    tags=["Seller Applications"],
)


@seller_application_router.post(
    "/",
    response_model=SellerApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_seller_application(
    application_data: CreateSellerApplication,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: SellerApplicationService = Depends(
        get_seller_application_service
    ),
):
    return service.create_application(
        db=db,
        application_data=application_data,
        current_user=current_user,
    )


@seller_application_router.get(
    "/me",
    response_model=SellerApplicationResponse,
)
def get_my_seller_application(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: SellerApplicationService = Depends(
        get_seller_application_service
    ),
):
    return service.get_my_application(
        db=db,
        current_user=current_user,
    )




@seller_application_router.get(
    "/",
    response_model=list[SellerApplicationResponse],
)
def get_all_seller_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
    service: SellerApplicationService = Depends(
        get_seller_application_service
    ),
):
    return service.get_all_applications(
        db=db
    )


@seller_application_router.patch(
    "/{application_id}/approve",
    response_model=SellerApplicationResponse,
)
def approve_seller_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
    service: SellerApplicationService = Depends(
        get_seller_application_service
    ),
):
    return service.approve_application(
        db=db,
        application_id=application_id,
    )


@seller_application_router.patch(
    "/{application_id}/reject",
    response_model=SellerApplicationResponse,
)
def reject_seller_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
    service: SellerApplicationService = Depends(
        get_seller_application_service
    ),
):
    return service.reject_application(
        db=db,
        application_id=application_id,
    )



