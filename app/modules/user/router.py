
from fastapi import APIRouter,  Depends
from app.modules.user.models import User
from app.core.dependencies import get_db

from app.modules.auth.dependencies import get_current_user
from app.modules.user.service import get_user_Profile
from sqlalchemy.orm import Session
from app.modules.user.schemas import UserResponse



user_router = APIRouter(tags=["User"], prefix="/user")



@user_router.get("/me", response_model=UserResponse)
async def auth_get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_Profile(db, current_user.id)

@user_router.put("/me", response_model=UserResponse )
async def auth_update_profile():
    pass

@user_router.delete("/me")
async def auth_change_password():
    pass



