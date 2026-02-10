from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


# Base schemas for classification tables
class ExerciseCategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    displacement: bool = False
    metabolic_type: str | None = Field(None, max_length=100)


class MovementTypeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class MuscleGroupBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class EquipmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class PositionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class ContractionTypeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


# Exercise base schema
class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    short_name: str | None = Field(None, max_length=50)
    description: str | None = None
    coach_id: UUID | None = None
    category_id: int | None = None
    movement_type_id: int | None = None
    muscle_group_id: int | None = None
    equipment_id: int | None = None
    position_id: int | None = None
    contraction_type_id: int | None = None
    type: str | None = Field(None, max_length=100)
    crossfit_variant: dict[str, Any] | None = None


# Create schemas
class ExerciseCategoryCreate(ExerciseCategoryBase):
    pass


class MovementTypeCreate(MovementTypeBase):
    pass


class MuscleGroupCreate(MuscleGroupBase):
    pass


class EquipmentCreate(EquipmentBase):
    pass


class PositionCreate(PositionBase):
    pass


class ContractionTypeCreate(ContractionTypeBase):
    pass


class ExerciseCreate(ExerciseBase):
    pass


# Update schemas (NUEVOS - AGREGAR ESTOS)
class ExerciseCategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    displacement: bool | None = None
    metabolic_type: str | None = Field(None, max_length=100)


class MovementTypeUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)


class MuscleGroupUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)


class EquipmentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)


class PositionUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)


class ContractionTypeUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)


class ExerciseUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    short_name: str | None = Field(None, max_length=50)
    description: str | None = None
    category_id: int | None = None
    movement_type_id: int | None = None
    muscle_group_id: int | None = None
    equipment_id: int | None = None
    position_id: int | None = None
    contraction_type_id: int | None = None
    type: str | None = Field(None, max_length=100)
    crossfit_variant: dict[str, Any] | None = None


# In DB schemas
class ExerciseCategoryInDB(ExerciseCategoryBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class MovementTypeInDB(MovementTypeBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class MuscleGroupInDB(MuscleGroupBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class EquipmentInDB(EquipmentBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class PositionInDB(PositionBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ContractionTypeInDB(ContractionTypeBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ExerciseInDB(ExerciseBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Response schemas with relationships
class ExerciseCategory(ExerciseCategoryInDB):
    pass


class MovementType(MovementTypeInDB):
    pass


class MuscleGroup(MuscleGroupInDB):
    pass


class Equipment(EquipmentInDB):
    pass


class Position(PositionInDB):
    pass


class ContractionType(ContractionTypeInDB):
    pass


class Exercise(ExerciseInDB):
    coach: Any | None = None  # Will be populated
    category: ExerciseCategory | None = None
    movement_type: MovementType | None = None
    muscle_group: MuscleGroup | None = None
    equipment: Equipment | None = None
    position: Position | None = None
    contraction_type: ContractionType | None = None


# List responses
class ExerciseList(BaseModel):
    exercises: list[Exercise]
    total: int
    page: int
    size: int


class ExerciseCategoriesList(BaseModel):
    categories: list[ExerciseCategory]
    total: int


class MovementTypesList(BaseModel):
    movement_types: list[MovementType]
    total: int


class MuscleGroupsList(BaseModel):
    muscle_groups: list[MuscleGroup]
    total: int


class EquipmentList(BaseModel):
    equipment: list[Equipment]
    total: int


class PositionsList(BaseModel):
    positions: list[Position]
    total: int


class ContractionTypesList(BaseModel):
    contraction_types: list[ContractionType]
    total: int
