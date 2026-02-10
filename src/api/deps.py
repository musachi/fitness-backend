from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import verify_token
from src.crud.user import user
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        user_obj = user.get(db, id=UUID(user_id))
        if user_obj is None:
            raise credentials_exception

    except (JWTError, ValueError):
        raise credentials_exception from None

    return user_obj


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get current active user
    Add additional checks here if needed (e.g., is_active flag)
    """
    # Example: if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_coach(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to ensure user is a coach
    Assuming role_id 2 is coach (adjust based on your roles table)
    """
    if current_user.role_id != 2:  # Adjust role_id as needed
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


def get_current_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to ensure user is an admin
    Assuming role_id 1 is admin
    """
    if current_user.role_id != 1:  # Adjust role_id as needed
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


def get_current_coach_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to ensure user is either a coach or an admin
    Assuming role_id 1 is admin and role_id 2 is coach
    """
    if current_user.role_id not in [1, 2]:  # Admin or Coach
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only coaches and admins can perform this action"
        )
    return current_user
