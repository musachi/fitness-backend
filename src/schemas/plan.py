from __future__ import annotations

from datetime import datetime, date
from enum import StrEnum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PlanGoal(StrEnum):
    MUSCLE_GAIN = "muscle_gain"
    WEIGHT_LOSS = "weight_loss"
    STRENGTH = "strength"
    ENDURANCE = "endurance"
    GENERAL_FITNESS = "general_fitness"


class PlanLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class WorkoutFocus(StrEnum):
    PUSH = "push"
    PULL = "pull"
    LEGS = "legs"
    FULL_BODY = "full_body"
    UPPER_BODY = "upper_body"
    LOWER_BODY = "lower_body"
    CARDIO = "cardio"
    REST = "rest"


# Base schemas
class PlanBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    duration_weeks: int = Field(..., ge=1, le=52)
    goal: PlanGoal
    level: PlanLevel
    description: Optional[str] = Field(None, max_length=1000)


class PlanCreate(PlanBase):
    is_template: bool = False
    is_public: bool = True


class PlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    duration_weeks: Optional[int] = Field(None, ge=1, le=52)
    goal: Optional[PlanGoal] = None
    level: Optional[PlanLevel] = None
    is_public: Optional[bool] = None


# Workout Session schemas
class WorkoutSessionBase(BaseModel):
    date: date
    notes: Optional[str] = Field(None, max_length=500)


class WorkoutSessionCreate(WorkoutSessionBase):
    plan_id: int


class WorkoutSessionUpdate(BaseModel):
    date: Optional[date] = None
    completed: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=500)


# Workout Exercise schemas
class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets_planned: int = Field(..., ge=1, le=10)
    reps_planned: str = Field(..., max_length=50)  # "8-12", "10", "AMRAP 15"
    weight_planned: Optional[str] = Field(None, max_length=50)  # "50kg", "bodyweight"
    rest_between_sets: Optional[str] = Field(None, max_length=50)  # "60s", "2min"


class WorkoutExerciseCreate(WorkoutExerciseBase):
    session_id: int


class WorkoutExerciseUpdate(BaseModel):
    sets_done: Optional[int] = Field(None, ge=0, le=20)
    reps_done: Optional[List[int]] = None
    weight_used: Optional[str] = Field(None, max_length=50)
    time_spent: Optional[str] = Field(None, max_length=50)
    reps_in_time: Optional[int] = Field(None, ge=0)


# Response schemas
class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    session_id: int
    sets_done: Optional[int] = None
    reps_done: Optional[List[int]] = None
    weight_used: Optional[str] = None
    time_spent: Optional[str] = None
    reps_in_time: Optional[int] = None

    class Config:
        from_attributes = True


class WorkoutSessionResponse(WorkoutSessionBase):
    id: int
    plan_id: int
    client_id: UUID
    completed: bool = False
    workout_exercises: List[WorkoutExerciseResponse] = []

    class Config:
        from_attributes = True


class PlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    goal: str
    level: str
    duration_weeks: int
    coach_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    workout_sessions: List[WorkoutSessionResponse] = []

    class Config:
        from_attributes = True


# Template schemas
class PlanTemplate(BaseModel):
    name: str
    description: str
    goal: PlanGoal
    level: PlanLevel
    duration_weeks: int
    workouts_per_week: int
    focus_rotation: List[WorkoutFocus]

    class Config:
        from_attributes = True


class PlanFromTemplateRequest(BaseModel):
    template_name: str
    custom_name: Optional[str] = None


class PlanFromTemplateResponse(BaseModel):
    plan_id: int
    name: str
    duration_weeks: int
    workouts_count: int
    message: str = "Plan generated successfully"


# List responses
class PlansList(BaseModel):
    plans: List[PlanResponse]


class WorkoutSessionsList(BaseModel):
    sessions: List[WorkoutSessionResponse]


class WorkoutExercisesList(BaseModel):
    exercises: List[WorkoutExerciseResponse]
