from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_current_admin
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

    # If user is requesting coach role, set is_approved to False
    user_data = user_in.dict()
    if user_data.get('role_id') == 2:  # Coach role
        user_data['is_approved'] = False
        user_data['approval_requested_at'] = datetime.utcnow()
    else:
        user_data['is_approved'] = True

    # Create new user
    new_user = user.create(db, obj_in=user_data)
    return new_user


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login using JSON data
    """
    # Authenticate user
    authenticated_user = user.authenticate(db, login_data=login_data)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Check if user is approved (for coaches)
    if authenticated_user.role_id == 2 and not authenticated_user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach account is pending approval. Please wait for admin approval.",
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(authenticated_user.id), "exp": access_token_expires.total_seconds(), "type": "access"}
    )

    return LoginResponse(
        user_id=authenticated_user.id,
        email=authenticated_user.email,
        name=authenticated_user.name,
        role_id=authenticated_user.role_id,
        access_token=access_token,
        token_type="bearer"
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


@router.get("/pending-coaches", response_model=list[User])
async def get_pending_coaches(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get list of coaches pending approval (Admin only)
    """
    pending_coaches = user.get_pending_coaches(db)
    return pending_coaches


@router.post("/approve-coach/{coach_id}")
async def approve_coach(
    coach_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Approve a coach account (Admin only)
    """
    coach_user = user.get(db, id=coach_id)
    if not coach_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )

    if coach_user.role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a coach"
        )

    if coach_user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coach is already approved"
        )

    # Approve the coach
    user.approve_coach(db, coach_id=coach_id, approved_by=current_user.id)

    return {"message": "Coach approved successfully"}
