import asyncio
from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.database import get_db
from src.main import app
from src.models.base import Base
from src.models.exercise import (
    ContractionType,
    Equipment,
    Exercise,
    ExerciseCategory,
    MovementType,
    MuscleGroup,
    Position,
)
from src.models.user import User

# Test database setup - using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of default event loop for test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with test database."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password",
        role_id=2,  # Coach role
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session: Session) -> User:
    """Create a test admin user."""
    admin_user = User(
        id=uuid4(),
        name="Admin User",
        email="admin@example.com",
        password_hash="hashed_password",
        role_id=1,  # Admin role
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)
    return admin_user


@pytest.fixture
def exercise_category(db_session: Session) -> ExerciseCategory:
    """Create a test exercise category."""
    category = ExerciseCategory(
        name="Strength", displacement=False, metabolic_type="anaerobic"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def movement_type(db_session: Session) -> MovementType:
    """Create a test movement type."""
    movement_type = MovementType(name="Compound")
    db_session.add(movement_type)
    db_session.commit()
    db_session.refresh(movement_type)
    return movement_type


@pytest.fixture
def muscle_group(db_session: Session) -> MuscleGroup:
    """Create a test muscle group."""
    muscle_group = MuscleGroup(name="Chest")
    db_session.add(muscle_group)
    db_session.commit()
    db_session.refresh(muscle_group)
    return muscle_group


@pytest.fixture
def equipment(db_session: Session) -> Equipment:
    """Create a test equipment."""
    equipment = Equipment(name="Barbell")
    db_session.add(equipment)
    db_session.commit()
    db_session.refresh(equipment)
    return equipment


@pytest.fixture
def position(db_session: Session) -> Position:
    """Create a test position."""
    position = Position(name="Standing")
    db_session.add(position)
    db_session.commit()
    db_session.refresh(position)
    return position


@pytest.fixture
def contraction_type(db_session: Session) -> ContractionType:
    """Create a test contraction type."""
    contraction_type = ContractionType(name="Concentric")
    db_session.add(contraction_type)
    db_session.commit()
    db_session.refresh(contraction_type)
    return contraction_type


@pytest.fixture
def test_exercise(
    db_session: Session,
    test_user: User,
    exercise_category: ExerciseCategory,
    movement_type: MovementType,
    muscle_group: MuscleGroup,
    equipment: Equipment,
    position: Position,
    contraction_type: ContractionType,
) -> Exercise:
    """Create a test exercise with all relations."""
    exercise = Exercise(
        name="Bench Press",
        short_name="BP",
        description="Classic chest exercise",
        coach_id=test_user.id,
        category_id=exercise_category.id,
        movement_type_id=movement_type.id,
        muscle_group_id=muscle_group.id,
        equipment_id=equipment.id,
        position_id=position.id,
        contraction_type_id=contraction_type.id,
        type="strength",
    )
    db_session.add(exercise)
    db_session.commit()
    db_session.refresh(exercise)
    return exercise


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Get authentication headers for test user."""
    # This would need to be implemented based on your auth system
    # For now, returning mock headers
    return {
        "Authorization": f"Bearer mock_token_for_{test_user.id}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def admin_auth_headers(test_admin_user: User) -> dict:
    """Get authentication headers for admin user."""
    # This would need to be implemented based on your auth system
    # For now, returning mock headers
    return {
        "Authorization": f"Bearer mock_token_for_{test_admin_user.id}",
        "Content-Type": "application/json",
    }
