


from app.core.exceptions import AppException


class InvalidPriceRangeException(AppException):
    status_code: int = 400  # Bad Request status code

    def __init__(self, min_price: float, max_price: float):
        message = f"Invalid price range: min_price ({min_price}) cannot be greater than max_price ({max_price})."
        super().__init__(message)

class ProductNotFoundException(AppException):
    status_code: int = 404  # Not Found status code

    def __init__(self, product_id: int):
        message = f"Product with ID {product_id} not found."
        super().__init__(message)