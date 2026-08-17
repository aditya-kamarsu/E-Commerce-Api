


from app.core.exceptions import AppException


class AddressNotFoundException(AppException):
    status_code: int = 404  # Not Found status code
    def __init__(self, address_id: int):
        message = f"Address with ID {address_id} not found."
        super().__init__(message)

class AddressAlreadyExistsException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, address_id: int):
        message = f"Address with ID {address_id} already exists."
        super().__init__(message)


class NotAuthorizedAddressAccessException(AppException):
    status_code: int = 403  # Forbidden status code
    def __init__(self, address_id: int):
        message = f"You are not authorized to access the address with ID {address_id}."
        super().__init__(message)