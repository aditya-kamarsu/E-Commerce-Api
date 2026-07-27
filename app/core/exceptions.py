




from decimal import Decimal

from fastapi import HTTPException

class AppException(HTTPException):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(
            status_code=self.status_code,
            detail=message
        )




class InvalidProductPriceException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, price: Decimal):
        message = f"Invalid product price: {price}. Price must be greater than zero."
        super().__init__(message)



class InvalidProductStockException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, stock: int):
        message = f"Invalid product stock: {stock}. Stock must be greater than or equal to zero."
        super().__init__(message)


class DuplicateProductException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, name: str):
        message = f"Product with name '{name}' already exists."
        super().__init__(message)

class ProductNotFoundException(AppException):
    status_code: int = 404  # Not Found status code
    def __init__(self, product_id: int):
        message = f"Product with ID {product_id} not found."
        super().__init__(message)


class PermissionDeniedException(AppException):
    status_code: int = 403  # Forbidden status code
    def __init__(self):
        message = "Permission denied. You do not have access to this resource."
        super().__init__(message)
        
class InvalidQuantityException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, quantity: int):
        message = f"Invalid quantity: {quantity}. Quantity must be greater than zero."
        super().__init__(message)

class ProductInactiveException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, product_id: int):
        message = f"Product with ID {product_id} is not available for purchase."
        super().__init__(message)
        

class InsufficientStockException(AppException):
    status_code: int = 400  # Bad Request status code
    def __init__(self, product_id: int, available_stock: int):
        message = f"Insufficient stock for product with ID {product_id}. Only {available_stock} items available."
        super().__init__(message)

class CartNotFoundException(AppException):
    status_code: int = 404  # Not Found status code
    def __init__(self, user_id: int):
        message = f"Cart for user with ID {user_id} not found."
        super().__init__(message)

class CartItemNotFoundException(AppException):
    status_code: int = 404  # Not Found status code
    def __init__(self, cart_id: int, product_id: int):
        message = f"Cart item for cart ID {cart_id} and product ID {product_id} not found."
        super().__init__(message)
        