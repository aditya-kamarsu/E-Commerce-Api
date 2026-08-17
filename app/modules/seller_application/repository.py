

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.seller_application.models import SellerApplication
from app.modules.seller_application.utils import SellerApplicationStatus


class SellerApplicationRepository:

    def create(
        self,
        db: Session,
        application: SellerApplication,
    ) -> SellerApplication:
        try:
            db.add(application)
            db.flush()
            db.refresh(application)
            return application
        except Exception:
            db.rollback()
            raise

    def get_by_id(
        self,
        db: Session,
        application_id: int,
    ) -> SellerApplication | None:

        stmt = select(SellerApplication).where(
            SellerApplication.id == application_id
        )

        return db.scalar(stmt)

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> SellerApplication | None:

        stmt = select(SellerApplication).where(
            SellerApplication.user_id == user_id
        )

        return db.scalar(stmt)

    def get_all(
        self,
        db: Session,
    ) -> list[SellerApplication]:

        stmt = (
            select(SellerApplication)
            .order_by(SellerApplication.created_at.desc())
        )

        return db.scalars(stmt).all()

    def get_by_status(
        self,
        db: Session,
        status: SellerApplicationStatus,
    ) -> list[SellerApplication]:

        stmt = (
            select(SellerApplication)
            .where(SellerApplication.status == status)
            .order_by(SellerApplication.created_at.desc())
        )

        return db.scalars(stmt).all()

    def update_status(
        self,
        db: Session,
        application: SellerApplication,
        status: SellerApplicationStatus,
    ) -> SellerApplication:

        try:
            application.status = status

            db.flush()
            db.refresh(application)

            return application

        except Exception:
            db.rollback()
            raise