

from app.core.exceptions import AppException


class DuplicateCategoryException(AppException):
    status_code: int = 400  # Bad Request status code

    def __init__(self, category_name: str):
        message = f"Category with name '{category_name}' already exists."
        super().__init__(message)


class CategoryNotFoundException(AppException):
    status_code: int = 404  # Not Found status code

    def __init__(self, category_id: int):
        message = f"Category with ID {category_id} not found."
        super().__init__(message)



class CategoryHasProductsException(AppException):
    status_code: int = 400  # Bad Request status code

    def __init__(self, category_id: int):
        message = f"Category with ID {category_id} has associated products and cannot be deleted."
        super().__init__(message)