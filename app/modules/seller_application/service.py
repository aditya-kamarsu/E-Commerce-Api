from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.seller_application.models import SellerApplication
from app.modules.seller_application.repository import SellerApplicationRepository
from app.modules.seller_application.schema import CreateSellerApplication
from app.modules.seller_application.utils import SellerApplicationStatus
from app.modules.user.models import User
from app.core.enums import UserRole


class SellerApplicationService:

    def __init__(
        self,
        seller_application_repository: SellerApplicationRepository,
    ):
        self.seller_application_repository = (
            seller_application_repository
        )

    def create_application(
        self,
        db: Session,
        application_data: CreateSellerApplication,
        current_user: User,
    ):
        try:
            # User is already a seller
            if current_user.role == UserRole.SELLER:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You are already a seller.",
                )

            # Admin doesn't need to apply
            if current_user.role == UserRole.ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Admin users cannot submit seller applications.",
                )

            # Check existing application
            existing_application = (
                self.seller_application_repository.get_by_user(
                    db=db,
                    user_id=current_user.id,
                )
            )

            if existing_application:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already submitted a seller application.",
                )

            application = SellerApplication(
                user_id=current_user.id,
                business_name=application_data.business_name,
                reason=application_data.reason,
                status=SellerApplicationStatus.PENDING,
            )

            application = (
                self.seller_application_repository.create(
                    db=db,
                    application=application,
                )
            )

            db.commit()

            return application

        except Exception:
            db.rollback()
            raise

    def get_my_application(
        self,
        db: Session,
        current_user: User,
    ):
        application = (
            self.seller_application_repository.get_by_user(
                db=db,
                user_id=current_user.id,
            )
        )

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller application not found.",
            )

        return application

    def get_all_applications(
        self,
        db: Session,
    ):
        return self.seller_application_repository.get_all(
            db=db
        )

    def approve_application(
        self,
        db: Session,
        application_id: int,
    ):
        try:
            application = (
                self.seller_application_repository.get_by_id(
                    db=db,
                    application_id=application_id,
                )
            )

            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Seller application not found.",
                )

            if application.status != SellerApplicationStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only pending applications can be approved.",
                )

            # Change application status
            application = (
                self.seller_application_repository.update_status(
                    db=db,
                    application=application,
                    status=SellerApplicationStatus.APPROVED,
                )
            )

            # Change user role
            user = application.user
            user.role = UserRole.SELLER

            db.flush()
            db.commit()

            return application

        except Exception:
            db.rollback()
            raise

    def reject_application(
        self,
        db: Session,
        application_id: int,
    ):
        try:
            application = (
                self.seller_application_repository.get_by_id(
                    db=db,
                    application_id=application_id,
                )
            )

            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Seller application not found.",
                )

            if application.status != SellerApplicationStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only pending applications can be rejected.",
                )

            application = (
                self.seller_application_repository.update_status(
                    db=db,
                    application=application,
                    status=SellerApplicationStatus.REJECTED,
                )
            )

            db.commit()

            return application

        except Exception:
            db.rollback()
            raise