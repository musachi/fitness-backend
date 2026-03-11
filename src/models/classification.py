from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import Base


class ClassificationType(Base):
    __tablename__ = "classification_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    applies_to = Column(String(20), nullable=False, default="exercises")  # exercises, plans, both
    is_required = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    classification_values = relationship("ClassificationValue", back_populates="classification_type", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ClassificationType(id={self.id}, name='{self.name}', applies_to='{self.applies_to}')>"


class ClassificationValue(Base):
    __tablename__ = "classification_values"

    id = Column(Integer, primary_key=True, index=True)
    classification_type_id = Column(Integer, ForeignKey("classification_types.id"), nullable=False)
    value = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    classification_type = relationship("ClassificationType", back_populates="classification_values")

    def __repr__(self):
        return f"<ClassificationValue(id={self.id}, value='{self.value}', order={self.order})>"
