from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.config import settings
from src.core.database import get_db
from src.core.security import create_access_token
from src.crud.user import user
from src.schemas.auth import LoginRequest, LoginResponse, Token
from src.schemas.user import User, UserRegister

router = APIRouter(tags=["authentication"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    new_user = user.create(db, obj_in=user_in)
    return new_user


@router.post("/login", response_model=LoginResponse)
async def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login using Form data
    """
    # Convert to our LoginRequest schema
    login_request = LoginRequest(email=username, password=password)

    # Authenticate user
    authenticated_user = user.authenticate(db, login_data=login_request)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(authenticated_user.id)}, expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=authenticated_user.id,
        email=authenticated_user.email,
        name=authenticated_user.name,
        role_id=authenticated_user.role_id,
    )


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
