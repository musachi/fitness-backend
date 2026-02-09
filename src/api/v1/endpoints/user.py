from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_current_admin, get_current_coach
from src.core.database import get_db
from src.crud.user import client_profile, user
from src.schemas.user import (
    ClientProfile,
    ClientProfileUpdate,
    User,
    UsersList,
    UserUpdate,
    UserWithProfile,
)

router = APIRouter(tags=["users"])


# Admin only endpoints
@router.get("/", response_model=UsersList, dependencies=[Depends(get_current_admin)])
async def read_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role_id: int | None = None,
    coach_id: UUID | None = None,
):
    """
    Retrieve users (Admin only)
    """
    # Build query based on filters
    query = db.query(user.model)

    if role_id:
        query = query.filter(user.model.role_id == role_id)
    if coach_id:
        query = query.filter(user.model.coach_id == coach_id)

    total = query.count()
    users_list = query.offset(skip).limit(limit).all()

    return UsersList(
        users=users_list,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=limit,
    )


@router.get("/{user_id}", response_model=UserWithProfile)
async def read_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get user by ID
    Users can see their own profile, coaches can see their clients, admins can see all
    """
    # Check permissions
    if (
        str(current_user.id) != str(user_id)
        and current_user.role_id not in [1, 2]  # Not own profile
        and current_user.id != user_id  # Not admin or coach  # Not coach of this client
    ):
        # Check if current user is coach of this client
        user_obj = user.get(db, id=user_id)
        if not user_obj or user_obj.coach_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )

    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user_obj


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update user
    Users can update their own profile, admins can update any
    """
    # Check permissions
    if str(current_user.id) != str(user_id) and current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    updated_user = user.update(db, db_obj=user_obj, obj_in=user_in)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # Admin only
):
    """
    Delete user (Admin only)
    """
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.remove(db, id=user_id)
    return None


# Client Profile endpoints
@router.get("/{user_id}/profile", response_model=ClientProfile)
async def get_client_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get client profile
    """
    # Check permissions
    if (
        str(current_user.id) != str(user_id)
        and current_user.role_id not in [1, 2]
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    profile = client_profile.get_by_user_id(db, user_id=user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    return profile


@router.put("/{user_id}/profile", response_model=ClientProfile)
async def update_client_profile(
    user_id: UUID,
    profile_in: ClientProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update client profile
    """
    # Check permissions
    if str(current_user.id) != str(user_id) and current_user.role_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    updated_profile = client_profile.update_or_create(
        db, user_id=user_id, obj_in=profile_in
    )
    return updated_profile


# Coach specific endpoints
@router.get(
    "/coach/clients",
    response_model=list[User],
    dependencies=[Depends(get_current_coach)],
)
async def get_coach_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_coach),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get clients assigned to current coach
    """
    clients = user.get_coach_clients(
        db, coach_id=current_user.id, skip=skip, limit=limit
    )
    return clients


@router.post("/search", response_model=list[User])
async def search_users(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Search users by name or email
    """
    if current_user.role_id not in [1, 2]:  # Only admin and coach
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    users_found = user.search_users(db, query=query, skip=skip, limit=limit)
    return users_found
