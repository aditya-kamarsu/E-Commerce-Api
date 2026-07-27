
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.dependencies import get_db
from app.modules.auth.jwt_token import ALGORITHM, SECRET_KEY
from app.modules.auth.jwt_token import decode_access_token
from jwt  import PyJWTError
from app.modules.auth.services import AuthService
from app.modules.user.repository import get_user_by_id
from sqlalchemy.orm import Session

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
        token: str = Depends(oauth_scheme),
        db: Session = Depends(get_db)

):
    credentials_exception = HTTPException(
        status_code  = 401,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        payload= payload.get("sub")
        user_id: int = int(payload)

        if user_id is None:
            raise credentials_exception
        
    except PyJWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id)

    if not user:
        raise credentials_exception

    return user





def get_authService():
    return AuthService()