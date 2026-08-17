

from app.core.exceptions import AppException




class ProductAlreadyInWishlistException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self,product_id: int):
        message = f"Product with ID {product_id} is already in the wishlist."
        super().__init__(message)




class WishlistItemNotFoundException(AppException):
    status_code: int = 404  # Not Found status code
    def __init__(self, product_id: int):
        message = f"Product with ID {product_id} not found in the wishlist."
        super().__init__(message)