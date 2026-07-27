



from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.modules.auth.jwt_token import create_access_token
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.modules.user.models import User
from app.modules.user.repository import get_by_email,create_user
from app.modules.auth.hashing import hash_password, verify_password



class AuthService():

    def register(self, db: Session, request: RegisterRequest):

        existing_user = get_by_email(db, request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = hash_password(request.password)

        # Create SQLAlchemy User object
        user = User(
            email=request.email,
            password_hash=hashed_password,
        )

        # Save user in database
        created_user = create_user(db,user)

        return created_user





    def login(self, db: Session, request: OAuth2PasswordRequestForm):
        user = get_by_email(db, request.username)  # Assuming the username field contains the email
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=token, token_type="bearer")

