from app.modules.addresses.schemas import CreateAddress,UpdateAddress
from sqlalchemy.orm import Session
from app.modules.user.models import User
from app.modules.addresses.models import Address
from app.modules.addresses.exceptions import AddressNotFoundException, NotAuthorizedAddressAccessException

class AddressService:

    def __init__(self, address_repository):
        self.address_repository = address_repository



    def create_address(
            self,
            db: Session,
            address_data:CreateAddress,
            current_user: User
    ):
        try:
            addresses = self.address_repository.get_by_user(
                db=db,
                user_id=current_user.id
            )

            is_first_address = len(addresses) == 0

            if is_first_address:
                address_data.is_default = True

            elif address_data.is_default:
                self.address_repository.clear_default(
                    db=db,
                    user_id=current_user.id
                )
            address = Address(
                **address_data.model_dump(),
                user_id=current_user.id
            )

            address = self.address_repository.create(
                db=db,
                address=address
            )

            db.commit()
            return address
        except Exception:
            db.rollback()
            raise



    def get_address_by_id(
            self,
            db: Session,
            address_id: int,
            current_user: User
    ):
        address = self.address_repository.get_by_id(
            db=db,
            address_id=address_id
        )
        if not address:
            raise AddressNotFoundException(address_id=address_id)
        if address.user_id != current_user.id:
            raise NotAuthorizedAddressAccessException(address_id=address_id)
        return address


    def get_user_addresses(
            self,
            db: Session,
            current_user: User
    ):
        return self.address_repository.get_by_user(
            db=db,
            user_id=current_user.id
        )


    def update_address(
            self,
            db: Session,
            address_id: int,
            address_update: UpdateAddress,
            current_user: User
    ):
        try:
            address = self.address_repository.get_by_id(
                db=db,
                address_id=address_id
            )
            if not address:
                raise AddressNotFoundException(address_id=address_id)
            if address.user_id != current_user.id:
                raise NotAuthorizedAddressAccessException(address_id=address_id)

            if address_update.is_default:
                self.address_repository.clear_default(
                    db=db,
                    user_id=current_user.id
                )

            address = self.address_repository.update(
                db=db,
                address_id=address_id,
                address_update=address_update,
              
            )
            db.commit()

            return address
        except Exception:
            db.rollback()
            raise


    def set_default_address(
        self,
        db: Session,
        address_id: int,
        current_user: User
    ):
        try:
            address = self.address_repository.get_by_id(
                db=db,
                address_id=address_id
            )

            if not address:
                raise AddressNotFoundException(
                    address_id=address_id
                )

            if address.user_id != current_user.id:
                raise NotAuthorizedAddressAccessException(
                    address_id=address_id
                )

            self.address_repository.clear_default(
                db=db,
                user_id=current_user.id
            )

            address.is_default = True

            db.commit()

            return address

        except Exception:
            db.rollback()
            raise

    def delete_address(
            self,
            db: Session,
            address_id: int,
            current_user: User
    ):
        try:
            address = self.address_repository.get_by_id(
                db=db,
                address_id=address_id
            )
            if not address:
                raise AddressNotFoundException(address_id=address_id)
            if address.user_id != current_user.id:
                raise NotAuthorizedAddressAccessException(address_id=address_id)

            self.address_repository.delete(
                db=db,
                address = address
            )
            db.commit()
            return {"message": f"Address with ID {address_id} has been deleted."}
        except Exception:
            db.rollback()
            raise
