from datetime import datetime

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Interval,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    goal = Column(String(50), nullable=False)  # muscle_gain, weight_loss, strength, etc.
    level = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    duration_weeks = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    coach_user = relationship("User", back_populates="created_plans")
    versions = relationship("PlanVersion", back_populates="plan")
    workout_sessions = relationship("WorkoutSession", back_populates="plan")
    subscriptions = relationship("Subscription", back_populates="plan")
    shared_plans = relationship("SharedPlan", back_populates="plan")


class PlanVersion(Base):
    __tablename__ = "plan_versions"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), index=True)
    version_number = Column(Integer, nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    plan = relationship("Plan", back_populates="versions")


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), index=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    notes = Column(String)

    # Relationships
    plan = relationship("Plan", back_populates="workout_sessions")
    client = relationship("User", back_populates="workout_sessions")
    workout_exercises = relationship("WorkoutExercise", back_populates="session")


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), index=True)
    sets_planned = Column(Integer)
    reps_planned = Column(String(50))
    weight_planned = Column(String(50))
    rest_between_sets = Column(String(50))
    sets_done = Column(Integer)
    reps_done = Column(JSON)  # Array de reps por set
    weight_used = Column(String(50))
    time_spent = Column(String(50))
    reps_in_time = Column(Integer)

    # Relationships
    session = relationship("WorkoutSession", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")

    # Continuación del mismo archivo


class ExerciseProgress(Base):
    __tablename__ = "exercise_progress"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), index=True)
    max_weight_lifted = Column(Integer)  # Cambié a INTEGER (kg)
    last_weight_used = Column(Integer)  # Cambié a INTEGER (kg)
    last_session_date = Column(Date)

    # Relationships
    client = relationship("User", back_populates="exercise_progress")
    exercise = relationship("Exercise", back_populates="exercise_progress")


class SharedExercise(Base):
    __tablename__ = "shared_exercises"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), index=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    can_edit = Column(Boolean, default=False)

    # Relationships
    exercise = relationship("Exercise", back_populates="shared_exercises")
    coach_user = relationship("User", back_populates="shared_exercises")


class SharedPlan(Base):
    __tablename__ = "shared_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), index=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    can_edit = Column(Boolean, default=False)

    # Relationships
    plan = relationship("Plan", back_populates="shared_plans")
    coach_user = relationship("User", back_populates="shared_plans")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String(20), default="active")
    payment_method = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")


class ClientAssessment(Base):
    __tablename__ = "client_assessments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    date = Column(Date, nullable=False)
    height = Column(Integer)  # Cambié a INTEGER (cm)
    weight = Column(Integer)  # Cambié a INTEGER (kg)
    neck = Column(Integer)  # Cambié a INTEGER (cm)
    waist = Column(Integer)  # Cambié a INTEGER (cm)
    hip = Column(Integer)  # Cambié a INTEGER (cm)
    bodyfat_percentage = Column(Integer)  # Cambié a INTEGER (%)
    bmi = Column(Integer)  # Cambié a INTEGER
    flexibility_test_score = Column(Integer)  # Cambié a INTEGER
    strength_test_score = Column(Integer)
    endurance_test_time = Column(Interval)  # Intervalo de tiempo
    notes = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    client = relationship("User", back_populates="assessments")
