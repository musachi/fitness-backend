from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> dict[str, Any]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return {}


# Optional: Add token type verification, expiration checks, etc. as needed


def sanitize_password(password: str, max_length: int = 72) -> str:
    """Sanitize password for bcrypt (max 72 bytes)"""
    # Convert to bytes and truncate
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > max_length:
        password_bytes = password_bytes[:max_length]
    return password_bytes.decode("utf-8", "ignore")


def get_password_hash(password: str) -> str:
    """Generate password hash with bcrypt limit handling"""
    # Sanitize password for bcrypt
    safe_password = sanitize_password(password)
    return pwd_context.hash(safe_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password with bcrypt limit handling"""
    safe_password = sanitize_password(plain_password)
    return pwd_context.verify(safe_password, hashed_password)
