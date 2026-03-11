from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


# Classification Type Schemas
class ClassificationTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    applies_to: str = Field(default="exercises", pattern="^(exercises|plans|both)$")
    is_required: bool = False


class ClassificationTypeCreate(ClassificationTypeBase):
    pass


class ClassificationTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    applies_to: Optional[str] = Field(None, pattern="^(exercises|plans|both)$")
    is_required: Optional[bool] = None
    
    # Custom validator to convert empty strings to None
    @validator('description', pre=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class ClassificationType(ClassificationTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    value_count: Optional[int] = 0

    class Config:
        from_attributes = True


# Classification Value Schemas
class ClassificationValueBase(BaseModel):
    classification_type_id: int
    value: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    order: int = Field(default=0, ge=0)


class ClassificationValueCreate(ClassificationValueBase):
    pass


class ClassificationValueUpdate(BaseModel):
    value: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)
    
    # Custom validator to convert empty strings to None
    @validator('description', pre=True)
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class ClassificationValue(ClassificationValueBase):
    id: int
    created_at: datetime
    updated_at: datetime
    classification_type: Optional[ClassificationType] = None

    class Config:
        from_attributes = True


# Response schemas with additional info
class ClassificationTypeWithValues(ClassificationType):
    classification_values: List[ClassificationValue] = []


class ClassificationValueWithType(ClassificationValue):
    classification_type: ClassificationType
