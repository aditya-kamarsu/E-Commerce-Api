
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.modules.user.models import UserRole



from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: EmailStr
    phone_number: str | None
    profile_image_url: str | None
    role: UserRole  
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UpdateProfileRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    profile_picture: str







