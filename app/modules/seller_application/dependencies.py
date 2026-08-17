from fastapi import Depends

from app.modules.seller_application.repository import SellerApplicationRepository
from app.modules.seller_application.service import SellerApplicationService


def get_seller_application_repository() -> SellerApplicationRepository:
    return SellerApplicationRepository()


def get_seller_application_service(
    seller_application_repository: SellerApplicationRepository = Depends(
        get_seller_application_repository
    ),
) -> SellerApplicationService:

    return SellerApplicationService(
        seller_application_repository=seller_application_repository,
    )