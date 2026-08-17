


from fastapi import Depends

from app.modules.addresses.repository import AddressRepository
from app.modules.addresses.service import AddressService

def get_address_repository() -> AddressRepository:
    return AddressRepository()

def get_address_service(
    address_repository: AddressRepository = Depends(get_address_repository)
):

    return AddressService(address_repository=address_repository)