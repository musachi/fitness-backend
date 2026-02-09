# Import all models here so they're registered with SQLAlchemy Base
from .base import Base, TimestampMixin
from .exercise import (
    ContractionType,
    Equipment,
    Exercise,
    ExerciseCategory,
    MovementType,
    MuscleGroup,
    Position,
)
from .plan import (
    ClientAssessment,
    ExerciseProgress,
    Plan,
    PlanVersion,
    SharedExercise,
    SharedPlan,
    Subscription,
    WorkoutExercise,
    WorkoutSession,
)
from .user import ClientProfile, CoachProfile, Role, User

# Export all models
__all__ = [
    "Base",
    "TimestampMixin",
    "Role",
    "User",
    "ClientProfile",
    "CoachProfile",
    "Exercise",
    "ExerciseCategory",
    "MovementType",
    "MuscleGroup",
    "Equipment",
    "Position",
    "ContractionType",
    "Plan",
    "PlanVersion",
    "WorkoutSession",
    "WorkoutExercise",
    "ExerciseProgress",
    "SharedExercise",
    "SharedPlan",
    "Subscription",
    "ClientAssessment",
]
