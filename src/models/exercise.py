from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

# Tabla intermedia para relaciones dinámicas
exercise_classifications = Table(
    'exercise_classifications',
    Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
    Column('classification_value_id', Integer, ForeignKey('classification_values.id'), primary_key=True),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)

# Tablas de clasificación (lookup tables)
class ExerciseCategory(Base):
    __tablename__ = "exercise_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    displacement = Column(Boolean, default=False)
    metabolic_type = Column(String(100))


class MovementType(Base):
    __tablename__ = "movement_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class ContractionType(Base):
    __tablename__ = "contraction_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50))
    description = Column(String)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    type = Column(String(100))
    crossfit_variant = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    coach_user = relationship("User", back_populates="created_exercises")
    
    # Relación dinámica con clasificaciones (como ExerciseDynamic)
    classification_values = relationship(
        "ClassificationValue", 
        secondary="exercise_classifications"
    )
    
    # Relaciones con workouts y progreso
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")
    exercise_progress = relationship("ExerciseProgress", back_populates="exercise")
    shared_exercises = relationship("SharedExercise", back_populates="exercise")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name})>"
    
    def get_classification_by_type(self, classification_type_name: str):
        """Obtener el valor de clasificación por tipo"""
        for classification_value in self.classification_values:
            if (classification_value.classification_type and 
                classification_value.classification_type.name == classification_type_name):
                return classification_value
        return None
    
    def get_classification_value_by_type(self, classification_type_name: str) -> str:
        """Obtener solo el valor (string) de la clasificación por tipo"""
        classification = self.get_classification_by_type(classification_type_name)
        return classification.value if classification else None
