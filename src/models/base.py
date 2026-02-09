from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr

from ..core.database import Base as BaseModel


class Base(BaseModel):
    """Base model with common columns"""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        """Convert class name to snake_case table name"""
        return cls.__name__.lower()


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
