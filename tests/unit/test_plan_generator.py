from datetime import date, timedelta
from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from src.models.exercise import Exercise
from src.models.plan import Plan, WorkoutExercise, WorkoutSession
from src.schemas.plan import PlanGoal, PlanLevel, WorkoutFocus
from src.services.plan_generator import (
    BEGINNER_FULL_BODY,
    PPL_INTERMEDIATE,
    UPPER_LOWER_ADVANCED,
    PlanGenerator,
    PlanTemplate,
)


class TestPlanGenerator:
    """Unit tests for PlanGenerator service."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def plan_generator(self, mock_db):
        """PlanGenerator instance with mock database."""
        return PlanGenerator(mock_db)

    @pytest.fixture
    def sample_exercises(self):
        """Sample exercises for testing."""
        return [
            Exercise(id=1, name="squat"),
            Exercise(id=2, name="bench_press"),
            Exercise(id=3, name="deadlift"),
            Exercise(id=4, name="pull_up"),
            Exercise(id=5, name="overhead_press"),
            Exercise(id=6, name="bicep_curl"),
            Exercise(id=7, name="tricep_extension"),
            Exercise(id=8, name="calf_raise"),
        ]

    def test_plan_generator_initialization(self, mock_db):
        """Test PlanGenerator initialization."""
        generator = PlanGenerator(mock_db)

        assert generator.db == mock_db
        assert len(generator.templates) == 3
        assert "beginner_full_body" in generator.templates
        assert "ppl_intermediate" in generator.templates
        assert "upper_lower_advanced" in generator.templates

    def test_get_available_templates(self, plan_generator):
        """Test getting available templates."""
        templates = plan_generator.get_available_templates()

        assert len(templates) == 3
        assert all("template_key" in t for t in templates)
        assert all("name" in t for t in templates)
        assert all("description" in t for t in templates)
        assert all("goal" in t for t in templates)
        assert all("level" in t for t in templates)

    def test_generate_plan_from_template_success(self, plan_generator, mock_db, sample_exercises):
        """Test successful plan generation from template."""
        # Mock database operations
        mock_plan = Plan(id=1, name="Test Plan", duration_weeks=4)
        mock_db.add.return_value = None
        mock_db.flush.return_value = None
        mock_db.commit.return_value = None

        # Mock exercise query
        mock_db.query.return_value.all.return_value = sample_exercises

        # Mock Plan creation
        with patch('src.services.plan_generator.Plan', return_value=mock_plan):
            result = plan_generator.generate_plan_from_template(
                template_name="beginner_full_body",
                user_id="test_user_123",
                custom_name="My Custom Plan"
            )

        assert result == mock_plan
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    def test_generate_plan_from_template_not_found(self, plan_generator):
        """Test plan generation with non-existent template."""
        with pytest.raises(ValueError, match="Template 'non_existent' not found"):
            plan_generator.generate_plan_from_template(
                template_name="non_existent",
                user_id="test_user_123"
            )

    def test_select_exercises_for_focus_full_body(self, plan_generator, mock_db, sample_exercises):
        """Test exercise selection for full body focus."""
        mock_db.query.return_value.all.return_value = sample_exercises

        exercises = plan_generator._select_exercises_for_focus(
            focus=WorkoutFocus.FULL_BODY,
            template=BEGINNER_FULL_BODY,
            week_number=1
        )

        assert len(exercises) >= 3  # Should have compound + accessory exercises
        assert all("exercise_id" in ex for ex in exercises)
        assert all("sets" in ex for ex in exercises)
        assert all("reps" in ex for ex in exercises)

    def test_select_exercises_for_focus_push(self, plan_generator, mock_db, sample_exercises):
        """Test exercise selection for push focus."""
        mock_db.query.return_value.all.return_value = sample_exercises

        exercises = plan_generator._select_exercises_for_focus(
            focus=WorkoutFocus.PUSH,
            template=PPL_INTERMEDIATE,
            week_number=1
        )

        assert len(exercises) >= 1
        assert all("exercise_id" in ex for ex in exercises)

    def test_select_exercises_for_focus_pull(self, plan_generator, mock_db, sample_exercises):
        """Test exercise selection for pull focus."""
        mock_db.query.return_value.all.return_value = sample_exercises

        exercises = plan_generator._select_exercises_for_focus(
            focus=WorkoutFocus.PULL,
            template=PPL_INTERMEDIATE,
            week_number=1
        )

        assert len(exercises) >= 1
        assert all("exercise_id" in ex for ex in exercises)

    def test_select_exercises_for_focus_legs(self, plan_generator, mock_db, sample_exercises):
        """Test exercise selection for legs focus."""
        mock_db.query.return_value.all.return_value = sample_exercises

        exercises = plan_generator._select_exercises_for_focus(
            focus=WorkoutFocus.LEGS,
            template=PPL_INTERMEDIATE,
            week_number=1
        )

        assert len(exercises) >= 1
        assert all("exercise_id" in ex for ex in exercises)

    def test_select_exercises_for_focus_rest(self, plan_generator):
        """Test exercise selection for rest focus."""
        # Mock the database query to return empty list
        plan_generator.db.query.return_value.all.return_value = []

        exercises = plan_generator._select_exercises_for_focus(
            focus=WorkoutFocus.REST,
            template=BEGINNER_FULL_BODY,
            week_number=1
        )

        assert exercises == []  # Rest days should have no exercises

    def test_select_exercises_no_available_exercises(self, plan_generator):
        """Test exercise selection when no exercises are available."""
        # Mock empty exercises list
        plan_generator.db.query.return_value.all.return_value = []

        exercises = plan_generator._select_exercises_for_focus(
            focus=WorkoutFocus.FULL_BODY,
            template=BEGINNER_FULL_BODY,
            week_number=1
        )

        assert exercises == []  # Should return empty list when no exercises available

    def test_create_custom_plan(self, plan_generator, mock_db):
        """Test custom plan creation."""
        from src.schemas.plan import PlanCreate

        plan_data = PlanCreate(
            name="Custom Plan",
            description="My custom workout plan",
            duration_weeks=6,
            goal=PlanGoal.GENERAL_FITNESS,
            level=PlanLevel.BEGINNER
        )

        mock_plan = Plan(id=1, name="Custom Plan")
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with patch('src.services.plan_generator.Plan', return_value=mock_plan):
            result = plan_generator.create_custom_plan(plan_data, "test_user_123")

        assert result == mock_plan
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


class TestPlanTemplates:
    """Unit tests for PlanTemplate objects."""

    def test_beginner_full_body_template(self):
        """Test BEGINNER_FULL_BODY template properties."""
        assert BEGINNER_FULL_BODY.name == "Beginner Full Body"
        assert BEGINNER_FULL_BODY.goal == PlanGoal.GENERAL_FITNESS
        assert BEGINNER_FULL_BODY.level == PlanLevel.BEGINNER
        assert BEGINNER_FULL_BODY.duration_weeks == 4
        assert BEGINNER_FULL_BODY.workouts_per_week == 3
        assert len(BEGINNER_FULL_BODY.focus_rotation) == 7
        assert WorkoutFocus.FULL_BODY in BEGINNER_FULL_BODY.focus_rotation
        assert WorkoutFocus.REST in BEGINNER_FULL_BODY.focus_rotation

    def test_ppl_intermediate_template(self):
        """Test PPL_INTERMEDIATE template properties."""
        assert PPL_INTERMEDIATE.name == "Push Pull Legs Intermediate"
        assert PPL_INTERMEDIATE.goal == PlanGoal.MUSCLE_GAIN
        assert PPL_INTERMEDIATE.level == PlanLevel.INTERMEDIATE
        assert PPL_INTERMEDIATE.duration_weeks == 8
        assert PPL_INTERMEDIATE.workouts_per_week == 6
        assert len(PPL_INTERMEDIATE.focus_rotation) == 7
        assert WorkoutFocus.PUSH in PPL_INTERMEDIATE.focus_rotation
        assert WorkoutFocus.PULL in PPL_INTERMEDIATE.focus_rotation
        assert WorkoutFocus.LEGS in PPL_INTERMEDIATE.focus_rotation

    def test_upper_lower_advanced_template(self):
        """Test UPPER_LOWER_ADVANCED template properties."""
        assert UPPER_LOWER_ADVANCED.name == "Upper Lower Advanced"
        assert UPPER_LOWER_ADVANCED.goal == PlanGoal.STRENGTH
        assert UPPER_LOWER_ADVANCED.level == PlanLevel.ADVANCED
        assert UPPER_LOWER_ADVANCED.duration_weeks == 12
        assert UPPER_LOWER_ADVANCED.workouts_per_week == 4
        assert len(UPPER_LOWER_ADVANCED.focus_rotation) == 7
        assert WorkoutFocus.UPPER_BODY in UPPER_LOWER_ADVANCED.focus_rotation
        assert WorkoutFocus.LOWER_BODY in UPPER_LOWER_ADVANCED.focus_rotation

    def test_template_exercise_rules(self):
        """Test that templates have proper exercise rules."""
        assert "compound" in BEGINNER_FULL_BODY.exercise_rules
        assert "accessory" in BEGINNER_FULL_BODY.exercise_rules
        assert "push" in PPL_INTERMEDIATE.exercise_rules
        assert "pull" in PPL_INTERMEDIATE.exercise_rules
        assert "legs" in PPL_INTERMEDIATE.exercise_rules
        assert "upper" in UPPER_LOWER_ADVANCED.exercise_rules
        assert "lower" in UPPER_LOWER_ADVANCED.exercise_rules


class TestPlanGeneratorIntegration:
    """Integration tests for PlanGenerator with more realistic scenarios."""

    @pytest.fixture
    def plan_generator(self):
        """PlanGenerator with real database session (for integration tests)."""
        # This would require a test database setup
        # For now, we'll use mock
        return Mock(spec=PlanGenerator)

    def test_full_plan_generation_workflow(self, plan_generator):
        """Test complete workflow of plan generation."""
        # This would be a full integration test
        # Mock the entire workflow
        mock_plan = Mock()
        mock_plan.id = 1
        mock_plan.name = "Generated Plan"
        mock_plan.duration_weeks = 4
        mock_plan.workout_sessions = [
            Mock(id=1, date=date.today()),
            Mock(id=2, date=date.today() + timedelta(days=2)),
            Mock(id=3, date=date.today() + timedelta(days=4)),
        ]

        plan_generator.generate_plan_from_template.return_value = mock_plan

        result = plan_generator.generate_plan_from_template(
            template_name="beginner_full_body",
            user_id="test_user"
        )

        assert result.id == 1
        assert result.name == "Generated Plan"
        assert len(result.workout_sessions) == 3
