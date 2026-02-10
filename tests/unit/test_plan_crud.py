from datetime import date
from unittest.mock import MagicMock, Mock
from uuid import uuid4

import pytest

from src.crud.plan import PlanCRUD, WorkoutExerciseCRUD, WorkoutSessionCRUD
from src.models.plan import Plan, WorkoutExercise, WorkoutSession
from src.schemas.plan import (
    PlanCreate,
    PlanUpdate,
    WorkoutSessionCreate,
    WorkoutSessionUpdate,
)


class TestPlanCRUD:
    """Unit tests for Plan CRUD operations."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def plan_crud(self, mock_db):
        """PlanCRUD instance with mock database."""
        return PlanCRUD(mock_db)

    @pytest.fixture
    def sample_plan(self):
        """Sample plan for testing."""
        return Plan(
            id=1,
            name="Test Plan",
            duration_weeks=4,
            coach_id=uuid4()
        )

    def test_get_plan_success(self, plan_crud, mock_db, sample_plan):
        """Test successful plan retrieval."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_plan
        mock_db.query.return_value = mock_query

        result = plan_crud.get(1)

        assert result == sample_plan
        mock_db.query.assert_called_once_with(Plan)
        mock_query.filter.assert_called_once_with(Plan.id == 1)
        mock_query.filter.return_value.first.assert_called_once()

    def test_get_plan_not_found(self, plan_crud, mock_db):
        """Test plan retrieval when not found."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query

        result = plan_crud.get(999)

        assert result is None

    def test_get_multi_plans(self, plan_crud, mock_db, sample_plan):
        """Test getting multiple plans."""
        mock_query = Mock()
        mock_query.filter.return_value.offset.return_value.limit.return_value = [sample_plan]
        mock_db.query.return_value = mock_query

        result = plan_crud.get_multi(skip=0, limit=100)

        assert result == [sample_plan]
        mock_query.offset.assert_called_once_with(0)
        mock_query.offset.return_value.limit.assert_called_once_with(100)

    def test_get_multi_plans_with_filters(self, plan_crud, mock_db, sample_plan):
        """Test getting multiple plans with filters."""
        coach_id = str(uuid4())
        mock_query = Mock()
        mock_query.filter.return_value.offset.return_value.limit.return_value = [sample_plan]
        mock_db.query.return_value = mock_query

        result = plan_crud.get_multi(
            skip=0,
            limit=100,
            coach_id=coach_id,
            is_public=True
        )

        assert result == [sample_plan]
        assert mock_query.filter.call_count == 2  # One for coach_id, one for is_public

    def test_get_by_user(self, plan_crud, mock_db, sample_plan):
        """Test getting plans by user."""
        user_id = str(uuid4())
        mock_query = Mock()
        mock_query.filter.return_value.offset.return_value.limit.return_value = [sample_plan]
        mock_db.query.return_value = mock_query

        result = plan_crud.get_by_user(user_id, skip=0, limit=100)

        assert result == [sample_plan]
        mock_query.filter.assert_called_once_with(Plan.coach_id == user_id)

    def test_get_public_plans(self, plan_crud, mock_db, sample_plan):
        """Test getting public plans."""
        mock_query = Mock()
        mock_query.filter.return_value.offset.return_value.limit.return_value = [sample_plan]
        mock_db.query.return_value = mock_query

        result = plan_crud.get_public_plans(skip=0, limit=100)

        assert result == [sample_plan]
        mock_query.filter.assert_called_once_with(Plan.is_public == True)

    def test_create_plan(self, plan_crud, mock_db):
        """Test creating a new plan."""
        plan_data = PlanCreate(
            name="New Plan",
            description="New Description",
            duration_weeks=6
        )
        coach_id = str(uuid4())

        mock_plan = Plan(
            id=1,
            name=plan_data.name,
            description=plan_data.description,
            duration_weeks=plan_data.duration_weeks,
            coach_id=coach_id
        )

        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with pytest.mock.patch('src.crud.plan.Plan', return_value=mock_plan):
            result = plan_crud.create(plan_data, coach_id)

        assert result == mock_plan
        mock_db.add.assert_called_once_with(mock_plan)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_plan)

    def test_update_plan(self, plan_crud, mock_db, sample_plan):
        """Test updating an existing plan."""
        update_data = PlanUpdate(
            name="Updated Plan"
        )

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_plan
        mock_db.query.return_value = mock_query

        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        result = plan_crud.update(1, update_data)

        assert result == sample_plan
        assert sample_plan.name == "Updated Plan"
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(sample_plan)

    def test_update_plan_not_found(self, plan_crud, mock_db):
        """Test updating a plan that doesn't exist."""
        update_data = PlanUpdate(name="Updated Plan")

        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query

        result = plan_crud.update(999, update_data)

        assert result is None

    def test_delete_plan(self, plan_crud, mock_db, sample_plan):
        """Test deleting a plan."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_plan
        mock_db.query.return_value = mock_query

        mock_db.delete.return_value = None
        mock_db.commit.return_value = None

        result = plan_crud.delete(1)

        assert result is True
        mock_db.delete.assert_called_once_with(sample_plan)
        mock_db.commit.assert_called_once()

    def test_delete_plan_not_found(self, plan_crud, mock_db):
        """Test deleting a plan that doesn't exist."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query

        result = plan_crud.delete(999)

        assert result is False

    def test_count_plans(self, plan_crud, mock_db):
        """Test counting plans."""
        mock_query = Mock()
        mock_query.filter.return_value.count.return_value = 5
        mock_db.query.return_value = mock_query

        result = plan_crud.count()

        assert result == 5
        mock_query.filter.return_value.count.assert_called_once()


class TestWorkoutSessionCRUD:
    """Unit tests for WorkoutSession CRUD operations."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def session_crud(self, mock_db):
        """WorkoutSessionCRUD instance with mock database."""
        return WorkoutSessionCRUD(mock_db)

    @pytest.fixture
    def sample_session(self):
        """Sample workout session for testing."""
        return WorkoutSession(
            id=1,
            plan_id=1,
            client_id=uuid4(),
            date=date.today(),
            completed=False,
            notes="Test session"
        )

    def test_get_session_success(self, session_crud, mock_db, sample_session):
        """Test successful session retrieval."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_session
        mock_db.query.return_value = mock_query

        result = session_crud.get(1)

        assert result == sample_session
        mock_db.query.assert_called_once_with(WorkoutSession)

    def test_get_by_plan(self, session_crud, mock_db, sample_session):
        """Test getting sessions by plan."""
        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.offset.return_value.limit.return_value = [sample_session]
        mock_db.query.return_value = mock_query

        result = session_crud.get_by_plan(1, skip=0, limit=100)

        assert result == [sample_session]
        mock_query.filter.assert_called_once_with(WorkoutSession.plan_id == 1)

    def test_get_by_client(self, session_crud, mock_db, sample_session):
        """Test getting sessions by client."""
        client_id = str(uuid4())
        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.offset.return_value.limit.return_value = [sample_session]
        mock_db.query.return_value = mock_query

        result = session_crud.get_by_client(client_id, skip=0, limit=100)

        assert result == [sample_session]
        mock_query.filter.assert_called_once_with(WorkoutSession.client_id == client_id)

    def test_create_session(self, session_crud, mock_db):
        """Test creating a new workout session."""
        session_data = WorkoutSessionCreate(
            plan_id=1,
            client_id=str(uuid4()),
            date=date.today(),
            notes="New session"
        )

        mock_session = WorkoutSession(
            id=1,
            plan_id=session_data.plan_id,
            client_id=session_data.client_id,
            date=session_data.date,
            notes=session_data.notes
        )

        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with pytest.mock.patch('src.crud.plan.WorkoutSession', return_value=mock_session):
            result = session_crud.create(session_data)

        assert result == mock_session
        mock_db.add.assert_called_once_with(mock_session)
        mock_db.commit.assert_called_once()

    def test_mark_completed(self, session_crud, mock_db, sample_session):
        """Test marking a session as completed."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_session
        mock_db.query.return_value = mock_query

        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        result = session_crud.mark_completed(1)

        assert result == sample_session
        assert sample_session.completed is True
        mock_db.commit.assert_called_once()


class TestWorkoutExerciseCRUD:
    """Unit tests for WorkoutExercise CRUD operations."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def exercise_crud(self, mock_db):
        """WorkoutExerciseCRUD instance with mock database."""
        return WorkoutExerciseCRUD(mock_db)

    @pytest.fixture
    def sample_exercise(self):
        """Sample workout exercise for testing."""
        return WorkoutExercise(
            id=1,
            session_id=1,
            exercise_id=1,
            sets_planned=3,
            reps_planned="8-12",
            weight_planned="50kg",
            rest_between_sets="60s"
        )

    def test_get_exercise_success(self, exercise_crud, mock_db, sample_exercise):
        """Test successful exercise retrieval."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_exercise
        mock_db.query.return_value = mock_query

        result = exercise_crud.get(1)

        assert result == sample_exercise
        mock_db.query.assert_called_once_with(WorkoutExercise)

    def test_get_by_session(self, exercise_crud, mock_db, sample_exercise):
        """Test getting exercises by session."""
        mock_query = Mock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = [sample_exercise]
        mock_db.query.return_value = mock_query

        result = exercise_crud.get_by_session(1)

        assert result == [sample_exercise]
        mock_query.filter.assert_called_once_with(WorkoutExercise.session_id == 1)

    def test_create_exercise(self, exercise_crud, mock_db):
        """Test creating a new workout exercise."""
        mock_exercise = WorkoutExercise(
            id=1,
            session_id=1,
            exercise_id=1,
            sets_planned=3,
            reps_planned="8-12"
        )

        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with pytest.mock.patch('src.crud.plan.WorkoutExercise', return_value=mock_exercise):
            result = exercise_crud.create(
                session_id=1,
                exercise_id=1,
                sets_planned=3,
                reps_planned="8-12"
            )

        assert result == mock_exercise
        mock_db.add.assert_called_once_with(mock_exercise)
        mock_db.commit.assert_called_once()

    def test_update_progress(self, exercise_crud, mock_db, sample_exercise):
        """Test updating exercise progress."""
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = sample_exercise
        mock_db.query.return_value = mock_query

        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        result = exercise_crud.update_progress(
            exercise_id=1,
            sets_done=3,
            reps_done=[10, 8, 8],
            weight_used="50kg"
        )

        assert result == sample_exercise
        assert sample_exercise.sets_done == 3
        assert sample_exercise.reps_done == [10, 8, 8]
        assert sample_exercise.weight_used == "50kg"
        mock_db.commit.assert_called_once()
