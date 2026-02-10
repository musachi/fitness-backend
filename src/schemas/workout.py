from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Workout Exercise schemas (para tracking en tiempo real)
class WorkoutExerciseTracking(BaseModel):
    """Schema para tracking de ejercicios durante un workout."""
    exercise_id: int
    exercise_name: str
    sets_planned: int
    reps_planned: str
    weight_planned: Optional[str] = None
    rest_between_sets: Optional[str] = None

    # Tracking data
    current_set: int = 0
    sets_completed: list[dict] = []
    is_completed: bool = False

    class Config:
        from_attributes = True


class WorkoutExerciseUpdate(BaseModel):
    """Schema para actualizar progreso de un ejercicio."""
    set_number: int = Field(..., ge=1)
    reps_completed: int = Field(..., ge=0)
    weight_used: Optional[str] = None
    notes: Optional[str] = None


# Workout Session schemas
class WorkoutSessionStart(BaseModel):
    """Schema para iniciar una sesión de workout."""
    session_id: int


class WorkoutSessionComplete(BaseModel):
    """Schema para completar una sesión de workout."""
    session_id: int
    notes: Optional[str] = None
    total_time: Optional[str] = None  # "45:30" formato MM:SS


class WorkoutSessionProgress(BaseModel):
    """Schema para mostrar progreso actual de una sesión."""
    session_id: int
    plan_name: str
    session_name: Optional[str] = None
    total_exercises: int
    completed_exercises: int
    current_exercise: Optional[WorkoutExerciseTracking] = None
    remaining_exercises: list[WorkoutExerciseTracking] = []
    progress_percentage: float = Field(..., ge=0, le=100)
    estimated_time_remaining: Optional[str] = None

    class Config:
        from_attributes = True


# Workout Plan Generation schemas
class WorkoutDay(BaseModel):
    """Schema para un día específico de entrenamiento."""
    day_number: int
    week_number: int
    name: str
    focus: str
    exercises: list[dict]  # Exercise data with sets/reps

    class Config:
        from_attributes = True


class WorkoutWeek(BaseModel):
    """Schema para una semana de entrenamiento."""
    week_number: int
    days: list[WorkoutDay]

    class Config:
        from_attributes = True


class WorkoutPlanStructure(BaseModel):
    """Schema para la estructura completa de un plan."""
    plan_id: int
    name: str
    duration_weeks: int
    weeks: list[WorkoutWeek]

    class Config:
        from_attributes = True


# Quick Workout schemas
class QuickWorkoutRequest(BaseModel):
    """Schema para crear un workout rápido."""
    focus: str  # "chest", "legs", "full_body", etc.
    duration_minutes: int = Field(..., ge=10, le=120)
    equipment_available: Optional[list[str]] = None
    difficulty_level: int = Field(3, ge=1, le=5)


class QuickWorkoutExercise(BaseModel):
    """Schema para ejercicio en workout rápido."""
    exercise_id: int
    exercise_name: str
    sets: int
    reps: str
    rest_time: str
    estimated_duration: str  # "5:30"

    class Config:
        from_attributes = True


class QuickWorkoutResponse(BaseModel):
    """Schema para respuesta de workout rápido generado."""
    workout_name: str
    total_duration: str
    exercises: list[QuickWorkoutExercise]
    warmup_suggestions: list[str]
    cooldown_suggestions: list[str]

    class Config:
        from_attributes = True
