from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.core.dependencies import get_db
from app.modules.auth.dependencies import get_authService
from app.modules.auth.schemas import LoginRequest, RegisterRequest, RegisterResponse, TokenResponse
from app.modules.auth.services import AuthService



auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



# @router.post("/register")
# async def register(request: RegisterRequest):
#     return await auth_service.register(request)



@auth_router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_authService)
):
   
   return service.register(db, request)

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    # request: LoginRequest,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_authService)
):
    return service.login(db, form_data)



 
