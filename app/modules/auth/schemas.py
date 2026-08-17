



from pydantic import BaseModel

from app.modules.user.schemas import UserResponse


class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    message: str = "User registered successfully"
    user: UserResponse


    
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  