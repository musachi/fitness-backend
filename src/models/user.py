import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String)
    is_paid = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    role = relationship("Role", back_populates="users")
    coach = relationship(
        "User", remote_side=[id], back_populates="clients", foreign_keys=[coach_id]
    )
    clients = relationship("User", back_populates="coach", foreign_keys=[coach_id])
    created_exercises = relationship("Exercise", back_populates="coach_user")
    created_plans = relationship("Plan", back_populates="coach_user")
    client_profile = relationship("ClientProfile", back_populates="user", uselist=False)
    assessments = relationship("ClientAssessment", back_populates="client")
    subscriptions = relationship("Subscription", back_populates="user")
    workout_sessions = relationship("WorkoutSession", back_populates="client")
    exercise_progress = relationship("ExerciseProgress", back_populates="client")
    shared_exercises = relationship("SharedExercise", back_populates="coach_user")
    shared_plans = relationship("SharedPlan", back_populates="coach_user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class ClientProfile(Base):
    __tablename__ = "clients_profile"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    height = Column(Integer)  # Cambié a INTEGER (cm)
    weight = Column(Integer)  # Cambié a INTEGER (kg)
    neck = Column(Integer)  # Cambié a INTEGER (cm)
    waist = Column(Integer)  # Cambié a INTEGER (cm)
    hip = Column(Integer)  # Cambié a INTEGER (cm)
    bodyfat_percentage = Column(Integer)  # Cambié a INTEGER (%)
    bmi = Column(Integer)  # Cambié a INTEGER
    goals = Column(String)  # Simplifiqué de ARRAY a TEXT (podemos usar JSON después)
    injuries = Column(String)  # Simplifiqué de ARRAY a TEXT
    medical_notes = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="client_profile")


class CoachProfile(Base):
    __tablename__ = "coach_profile"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    specialization = Column(String(255))
    certification = Column(String)
    experience_years = Column(Integer)
    hourly_rate = Column(Integer)
    bio = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<CoachProfile(user_id={self.user_id})>"
