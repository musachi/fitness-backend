from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

if TYPE_CHECKING:
    from .user import User


# Enums
class RoleName(StrEnum):
    ADMIN = "admin"
    COACH = "coach"
    CLIENT = "client"
    FREE_CLIENT = "free_client"
    PAID_CLIENT = "paid_client"


# Base schemas
class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = None
    is_paid: bool = False


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr = Field(..., max_length=255)
    role_id: int | None = None
    coach_id: UUID | None = None


# Create schemas
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=6)
    role_id: int = Field(default=3)  # Default to CLIENT


class RoleCreate(RoleBase):
    pass


# Update schemas
class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)
    role_id: int | None = None
    coach_id: UUID | None = None


class RoleUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    description: str | None = None
    is_paid: bool | None = None


# In DB schemas
class RoleInDB(RoleBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: UUID
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# Response schemas
class Role(RoleInDB):
    pass


class User(UserInDB):
    role: Role | None = None
    coach: User | None = None


# Client Profile schemas
class ClientProfileBase(BaseModel):
    height: int | None = Field(None, ge=50, le=250)  # cm
    weight: int | None = Field(None, ge=20, le=300)  # kg
    neck: int | None = Field(None, ge=20, le=60)  # cm
    waist: int | None = Field(None, ge=50, le=150)  # cm
    hip: int | None = Field(None, ge=60, le=200)  # cm
    bodyfat_percentage: int | None = Field(None, ge=3, le=60)  # %
    bmi: int | None = Field(None, ge=10, le=60)
    goals: str | None = None
    injuries: str | None = None
    medical_notes: str | None = None


class ClientProfileCreate(ClientProfileBase):
    user_id: UUID


class ClientProfileUpdate(ClientProfileBase):
    pass


class ClientProfile(ClientProfileBase):
    user_id: UUID
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# Full User with Profile
class UserWithProfile(User):
    client_profile: ClientProfile | None = None


# List response
class UsersList(BaseModel):
    users: list[User]
    total: int
    page: int
    size: int
