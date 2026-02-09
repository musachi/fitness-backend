from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: UUID | None = None
    exp: int | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginResponse(Token):
    user_id: UUID
    email: EmailStr
    name: str
    role_id: int | None


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

    # OAuth2 compatible login request


class OAuth2LoginRequest(BaseModel):
    username: str  # Email in our case
    password: str
    grant_type: str | None = "password"
    scope: str | None = ""
    client_id: str | None = None
    client_secret: str | None = None
