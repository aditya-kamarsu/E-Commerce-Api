

from app.core.exceptions import AppException


class InvalidCredentialsException(AppException):
    status_code: int = 401  # Unauthorized status code
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)