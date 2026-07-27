
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.modules.user.models import UserRole




class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr 
    first_name: str
    last_name: str
    phone_number: str
    profile_image_url: Optional[str] = None
    role: UserRole
    is_active: bool
    is_verified: bool                       
    created_at: datetime
    updated_at: datetime

class UpdateProfileRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    profile_picture: str







