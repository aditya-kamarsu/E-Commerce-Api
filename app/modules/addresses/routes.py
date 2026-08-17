



from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.addresses.dependencies import get_address_service
from app.modules.addresses.schemas import (
    CreateAddress,
    UpdateAddress,
    AddressResponse,
)
from app.modules.addresses.service import AddressService
from app.modules.user.models import User


address_router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)






@address_router.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED
)
def create_address(
    address_data: CreateAddress,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    address_service: AddressService = Depends(get_address_service)
):
    return address_service.create_address(
        db=db,
        address_data=address_data,
        current_user=current_user
    )













@address_router.get(
    "/",
    response_model=list[AddressResponse],
    status_code=status.HTTP_200_OK
)
def get_user_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    address_service: AddressService = Depends(get_address_service)
):
    return address_service.get_user_addresses(
        db=db,
        current_user=current_user
    )
















@address_router.get(
    "/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    address_service: AddressService = Depends(get_address_service)
):
    return address_service.get_address_by_id(
        db=db,
        address_id=address_id,
        current_user=current_user
    )


















@address_router.patch(
    "/{address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK
)
def update_address(
    address_id: int,
    address_update: UpdateAddress,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    address_service: AddressService = Depends(get_address_service)
):
    return address_service.update_address(
        db=db,
        address_id=address_id,
        address_update=address_update,
        current_user=current_user
    )











@address_router.patch(
    "/{address_id}/default",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK
)
def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    address_service: AddressService = Depends(get_address_service)
):
    return address_service.set_default_address(
        db=db,
        address_id=address_id,
        current_user=current_user
    )









@address_router.delete(
    "/{address_id}",
    status_code=status.HTTP_200_OK
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    address_service: AddressService = Depends(get_address_service)
):
    return address_service.delete_address(
        db=db,
        address_id=address_id,
        current_user=current_user
    )