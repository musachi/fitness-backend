from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.core.security import get_password_hash, verify_password
from src.models.user import ClientProfile, CoachProfile, Role, User
from src.schemas.auth import LoginRequest
from src.schemas.user import (
    ClientProfileCreate,
    ClientProfileUpdate,
    RoleCreate,
    RoleUpdate,
    UserCreate,
    UserUpdate,
)

from .base import CRUDBase


# CRUD for Role
class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Role | None:
        """Get role by name"""
        return db.query(Role).filter(Role.name == name).first()

    def get_paid_roles(self, db: Session) -> list[Role]:
        """Get all paid roles"""
        return db.query(Role).filter(Role.is_paid).all()


role = CRUDRole(Role)


# CRUD for User
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    def get_by_role(
        self, db: Session, *, role_id: int, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get users by role"""
        return (
            db.query(User)
            .filter(User.role_id == role_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_coach_clients(
        self, db: Session, *, coach_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get clients of a specific coach"""
        return (
            db.query(User)
            .filter(
                User.coach_id == coach_id, User.role_id.in_([3, 4, 5])  # Client roles
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create user with hashed password"""
        # Hash password
        hashed_password = get_password_hash(obj_in.password)

        # Create user data dict
        user_data = obj_in.dict(exclude={"password"})
        user_data["password_hash"] = hashed_password

        # Create user
        db_obj = User(**user_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user, handling password hashing"""
        update_data = obj_in.dict(exclude_unset=True)

        # Hash password if being updated
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password_hash"] = hashed_password
            del update_data["password"]

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, login_data: LoginRequest) -> User | None:
        """Authenticate user"""
        user = self.get_by_email(db, email=login_data.email)
        if not user:
            return None
        if not verify_password(login_data.password, user.password_hash):
            return None
        return user

    def search_users(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Search users by name or email"""
        return (
            db.query(User)
            .filter(or_(User.name.ilike(f"%{query}%"), User.email.ilike(f"%{query}%")))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending_coaches(self, db: Session) -> list[User]:
        """Get all coaches pending approval"""
        return (
            db.query(User)
            .filter(User.role_id == 2, User.is_approved == False)
            .all()
        )

    def approve_coach(self, db: Session, *, coach_id: str, approved_by: str) -> User:
        """Approve a coach account"""
        from datetime import datetime

        coach = self.get(db, id=coach_id)
        if not coach:
            return None

        coach.is_approved = True
        coach.approved_by = approved_by
        coach.approved_at = datetime.utcnow()

        db.commit()
        db.refresh(coach)
        return coach


user = CRUDUser(User)


# CRUD for ClientProfile
class CRUDClientProfile(
    CRUDBase[ClientProfile, ClientProfileCreate, ClientProfileUpdate]
):
    def get_by_user_id(self, db: Session, *, user_id: UUID) -> ClientProfile | None:
        """Get profile by user ID"""
        return db.query(ClientProfile).filter(ClientProfile.user_id == user_id).first()

    def update_or_create(
        self, db: Session, *, user_id: UUID, obj_in: ClientProfileUpdate
    ) -> ClientProfile:
        """Update existing profile or create if doesn't exist"""
        profile = self.get_by_user_id(db, user_id=user_id)

        if profile:
            return self.update(db, db_obj=profile, obj_in=obj_in)
        else:
            # Create new profile
            profile_data = obj_in.dict()
            profile_data["user_id"] = user_id
            return self.create(db, obj_in=ClientProfileCreate(**profile_data))


client_profile = CRUDClientProfile(ClientProfile)


# CRUD for CoachProfile
class CRUDCoachProfile(
    CRUDBase[CoachProfile, ClientProfileCreate, ClientProfileUpdate]
):
    def get_by_user_id(self, db: Session, *, user_id: UUID) -> CoachProfile | None:
        """Get coach profile by user ID"""
        return db.query(CoachProfile).filter(CoachProfile.user_id == user_id).first()

    def get_coaches_by_specialization(
        self, db: Session, *, specialization: str, skip: int = 0, limit: int = 100
    ) -> list[CoachProfile]:
        """Get coaches by specialization"""
        return (
            db.query(CoachProfile)
            .filter(CoachProfile.specialization.ilike(f"%{specialization}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_or_create(
        self,
        db: Session,
        *,
        user_id: UUID,
        obj_in: ClientProfileUpdate,  # Reusing same schema for simplicity
    ) -> CoachProfile:
        """Update existing coach profile or create if doesn't exist"""
        profile = self.get_by_user_id(db, user_id=user_id)

        if profile:
            return self.update(db, db_obj=profile, obj_in=obj_in)
        else:
            # Create new profile
            profile_data = obj_in.dict()
            profile_data["user_id"] = user_id
            return self.create(db, obj_in=ClientProfileCreate(**profile_data))


coach_profile = CRUDCoachProfile(CoachProfile)
