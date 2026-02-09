from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


# Tablas de clasificación (lookup tables)
class ExerciseCategory(Base):
    __tablename__ = "exercise_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    displacement = Column(Boolean, default=False)
    metabolic_type = Column(String(100))

    # Relationships
    exercises = relationship("Exercise", back_populates="category")


class MovementType(Base):
    __tablename__ = "movement_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    exercises = relationship("Exercise", back_populates="movement_type")


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    exercises = relationship("Exercise", back_populates="muscle_group")


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    exercises = relationship("Exercise", back_populates="equipment")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    exercises = relationship("Exercise", back_populates="position")


class ContractionType(Base):
    __tablename__ = "contraction_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    exercises = relationship("Exercise", back_populates="contraction_type")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50))
    description = Column(String)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    category_id = Column(Integer, ForeignKey("exercise_categories.id"))
    movement_type_id = Column(Integer, ForeignKey("movement_types.id"))
    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    contraction_type_id = Column(Integer, ForeignKey("contraction_types.id"))
    type = Column(String(100))
    crossfit_variant = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    coach_user = relationship("User", back_populates="created_exercises")
    category = relationship("ExerciseCategory", back_populates="exercises")
    movement_type = relationship("MovementType", back_populates="exercises")
    muscle_group = relationship("MuscleGroup", back_populates="exercises")
    equipment = relationship("Equipment", back_populates="exercises")
    position = relationship("Position", back_populates="exercises")
    contraction_type = relationship("ContractionType", back_populates="exercises")
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")
    exercise_progress = relationship("ExerciseProgress", back_populates="exercise")
    shared_exercises = relationship("SharedExercise", back_populates="exercise")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name})>"
