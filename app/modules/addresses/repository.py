

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.modules.addresses.models import Address
from app.modules.addresses.schemas import UpdateAddress




class AddressRepository:

    def create(
        self,
        db: Session,
        address: Address
    ) -> Address:
        try:
            db.add(address)
            db.flush()
            db.refresh(address)
            return address
        except Exception:
            db.rollback()
            raise





    def get_by_id(
        self,
        db: Session,
        address_id: int
    ) -> Address | None:

        stmt = (
            select(Address)
            .where(Address.id == address_id)
        )

        return db.scalar(stmt)



    

    def get_by_user(
        self,
        db: Session,
        user_id: int
    ) -> list[Address]:

        stmt = (
            select(Address)
            .where(Address.user_id == user_id)
            .order_by(Address.is_default.desc(), Address.created_at.desc())
        )

        return db.scalars(stmt).all()





    

    def get_default_by_user(
        self,
        db: Session,
        user_id: int
    ) -> Address | None:

        stmt = (
            select(Address)
            .where(
                Address.user_id == user_id,
                Address.is_default.is_(True)
            )
        )

        return db.scalar(stmt)


    

    def clear_default(
        self,
        db: Session,
        user_id: int
    ) -> None:

        stmt = (
            select(Address)
            .where(
                Address.user_id == user_id,
                Address.is_default.is_(True)
            )
        )

        addresses = db.scalars(stmt).all()

        for address in addresses:
            address.is_default = False

        db.flush()





    def update(
        self,
        db: Session,
        address_id: int,
        address_update: UpdateAddress
    ) -> Address | None:

        address = self.get_by_id(db, address_id)

        if not address:
            return None

        update_data = address_update.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(address, key, value)

        try:
            db.flush()
            db.refresh(address)
            return address
        except Exception:
            db.rollback()
            raise




    def delete(
        self,
        db: Session,
        address: Address
    ) -> bool:

        try:
            db.delete(address)
            db.flush()
            return True
        except Exception:
            db.rollback()
            raise