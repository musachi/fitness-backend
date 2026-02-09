from sqlalchemy.orm import Session

from src.crud.exercise import (
    contraction_type,
    equipment,
    exercise,
    exercise_category,
    movement_type,
    muscle_group,
    position,
)
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
from src.schemas.exercise import (
    ContractionTypeCreate,
    EquipmentCreate,
    ExerciseCategoryCreate,
    ExerciseCategoryUpdate,
    ExerciseCreate,
    ExerciseUpdate,
    MovementTypeCreate,
    MuscleGroupCreate,
    PositionCreate,
)


class TestExerciseCRUD:
    """Test suite for Exercise CRUD operations."""

    def test_create_exercise(self, db_session: Session, test_user: User):
        """Test creating an exercise."""
        exercise_data = ExerciseCreate(
            name="Test Exercise",
            short_name="TE",
            description="Test description",
            type="strength",
        )
        created_exercise = exercise.create_with_relations(
            db_session, obj_in=exercise_data, coach_id=test_user.id
        )

        assert created_exercise.name == "Test Exercise"
        assert created_exercise.short_name == "TE"
        assert created_exercise.coach_id == test_user.id
        assert created_exercise.type == "strength"

    def test_get_exercise(self, db_session: Session, test_exercise: Exercise):
        """Test getting an exercise by ID."""
        retrieved_exercise = exercise.get(db_session, id=test_exercise.id)
        assert retrieved_exercise is not None
        assert retrieved_exercise.id == test_exercise.id
        assert retrieved_exercise.name == test_exercise.name

    def test_get_exercise_not_found(self, db_session: Session):
        """Test getting a non-existent exercise."""
        retrieved_exercise = exercise.get(db_session, id=99999)
        assert retrieved_exercise is None

    def test_get_exercise_with_relations(
        self, db_session: Session, test_exercise: Exercise
    ):
        """Test getting an exercise with all relations loaded."""
        retrieved_exercise = exercise.get_with_relations(
            db_session, id=test_exercise.id
        )
        assert retrieved_exercise is not None
        assert retrieved_exercise.category is not None
        assert retrieved_exercise.muscle_group is not None
        assert retrieved_exercise.equipment is not None

    def test_get_multi_exercises(self, db_session: Session, test_user: User):
        """Test getting multiple exercises."""
        # Create multiple exercises
        for i in range(5):
            exercise_data = ExerciseCreate(name=f"Exercise {i}")
            exercise.create_with_relations(
                db_session, obj_in=exercise_data, coach_id=test_user.id
            )

        exercises = exercise.get_multi(db_session, skip=0, limit=10)
        assert len(exercises) == 5

    def test_update_exercise(self, db_session: Session, test_exercise: Exercise):
        """Test updating an exercise."""
        update_data = ExerciseUpdate(
            name="Updated Exercise", description="Updated description"
        )
        updated_exercise = exercise.update(
            db_session, db_obj=test_exercise, obj_in=update_data
        )

        assert updated_exercise.name == "Updated Exercise"
        assert updated_exercise.description == "Updated description"

    def test_delete_exercise(self, db_session: Session, test_exercise: Exercise):
        """Test deleting an exercise."""
        exercise_id = test_exercise.id
        exercise.remove(db_session, id=exercise_id)

        deleted_exercise = exercise.get(db_session, id=exercise_id)
        assert deleted_exercise is None

    def test_search_exercises(self, db_session: Session, test_exercise: Exercise):
        """Test searching exercises."""
        results = exercise.search_exercises(db_session, query="Bench")
        assert len(results) == 1
        assert "Bench" in results[0].name

    def test_get_exercises_by_coach(
        self, db_session: Session, test_exercise: Exercise, test_user: User
    ):
        """Test getting exercises by coach."""
        exercises = exercise.get_by_coach(db_session, coach_id=test_user.id)
        assert len(exercises) == 1
        assert exercises[0].coach_id == test_user.id

    def test_count_exercises(self, db_session: Session, test_user: User):
        """Test counting exercises."""
        # Create multiple exercises
        for i in range(3):
            exercise_data = ExerciseCreate(name=f"Exercise {i}")
            exercise.create_with_relations(
                db_session, obj_in=exercise_data, coach_id=test_user.id
            )

        count = exercise.count(db_session)
        assert count == 3


class TestExerciseCategoryCRUD:
    """Test suite for ExerciseCategory CRUD operations."""

    def test_create_category(self, db_session: Session):
        """Test creating an exercise category."""
        category_data = ExerciseCategoryCreate(
            name="Test Category", displacement=True, metabolic_type="aerobic"
        )
        created_category = exercise_category.create(db_session, obj_in=category_data)

        assert created_category.name == "Test Category"
        assert created_category.displacement is True
        assert created_category.metabolic_type == "aerobic"

    def test_get_category_by_name(
        self, db_session: Session, exercise_category: ExerciseCategory
    ):
        """Test getting a category by name."""
        retrieved_category = exercise_category.get_by_name(
            db_session, name=exercise_category.name
        )
        assert retrieved_category is not None
        assert retrieved_category.id == exercise_category.id

    def test_get_category_by_name_not_found(self, db_session: Session):
        """Test getting a non-existent category by name."""
        retrieved_category = exercise_category.get_by_name(
            db_session, name="Non-existent"
        )
        assert retrieved_category is None

    def test_get_categories_with_displacement(self, db_session: Session):
        """Test getting categories with displacement."""
        # Create categories with and without displacement
        cat1 = ExerciseCategory(name="With Displacement", displacement=True)
        cat2 = ExerciseCategory(name="Without Displacement", displacement=False)
        db_session.add_all([cat1, cat2])
        db_session.commit()

        categories_with_displacement = exercise_category.get_with_displacement(
            db_session
        )
        assert len(categories_with_displacement) == 1
        assert categories_with_displacement[0].displacement is True

    def test_update_category(
        self, db_session: Session, exercise_category: ExerciseCategory
    ):
        """Test updating a category."""
        update_data = ExerciseCategoryUpdate(name="Updated Category", displacement=True)
        updated_category = exercise_category.update(
            db_session, db_obj=exercise_category, obj_in=update_data
        )

        assert updated_category.name == "Updated Category"
        assert updated_category.displacement is True


class TestMovementTypeCRUD:
    """Test suite for MovementType CRUD operations."""

    def test_create_movement_type(self, db_session: Session):
        """Test creating a movement type."""
        movement_type_data = MovementTypeCreate(name="Test Movement")
        created_movement_type = movement_type.create(
            db_session, obj_in=movement_type_data
        )

        assert created_movement_type.name == "Test Movement"

    def test_get_movement_type_by_name(
        self, db_session: Session, movement_type: MovementType
    ):
        """Test getting a movement type by name."""
        retrieved_movement_type = movement_type.get_by_name(
            db_session, name=movement_type.name
        )
        assert retrieved_movement_type is not None
        assert retrieved_movement_type.id == movement_type.id


class TestMuscleGroupCRUD:
    """Test suite for MuscleGroup CRUD operations."""

    def test_create_muscle_group(self, db_session: Session):
        """Test creating a muscle group."""
        muscle_group_data = MuscleGroupCreate(name="Test Muscle Group")
        created_muscle_group = muscle_group.create(db_session, obj_in=muscle_group_data)

        assert created_muscle_group.name == "Test Muscle Group"

    def test_get_muscle_group_by_name(
        self, db_session: Session, muscle_group: MuscleGroup
    ):
        """Test getting a muscle group by name."""
        retrieved_muscle_group = muscle_group.get_by_name(
            db_session, name=muscle_group.name
        )
        assert retrieved_muscle_group is not None
        assert retrieved_muscle_group.id == muscle_group.id


class TestEquipmentCRUD:
    """Test suite for Equipment CRUD operations."""

    def test_create_equipment(self, db_session: Session):
        """Test creating equipment."""
        equipment_data = EquipmentCreate(name="Test Equipment")
        created_equipment = equipment.create(db_session, obj_in=equipment_data)

        assert created_equipment.name == "Test Equipment"

    def test_get_equipment_by_name(self, db_session: Session, equipment: Equipment):
        """Test getting equipment by name."""
        retrieved_equipment = equipment.get_by_name(db_session, name=equipment.name)
        assert retrieved_equipment is not None
        assert retrieved_equipment.id == equipment.id


class TestPositionCRUD:
    """Test suite for Position CRUD operations."""

    def test_create_position(self, db_session: Session):
        """Test creating a position."""
        position_data = PositionCreate(name="Test Position")
        created_position = position.create(db_session, obj_in=position_data)

        assert created_position.name == "Test Position"

    def test_get_position_by_name(self, db_session: Session, position: Position):
        """Test getting a position by name."""
        retrieved_position = position.get_by_name(db_session, name=position.name)
        assert retrieved_position is not None
        assert retrieved_position.id == position.id


class TestContractionTypeCRUD:
    """Test suite for ContractionType CRUD operations."""

    def test_create_contraction_type(self, db_session: Session):
        """Test creating a contraction type."""
        contraction_type_data = ContractionTypeCreate(name="Test Contraction")
        created_contraction_type = contraction_type.create(
            db_session, obj_in=contraction_type_data
        )

        assert created_contraction_type.name == "Test Contraction"

    def test_get_contraction_type_by_name(
        self, db_session: Session, contraction_type: ContractionType
    ):
        """Test getting a contraction type by name."""
        retrieved_contraction_type = contraction_type.get_by_name(
            db_session, name=contraction_type.name
        )
        assert retrieved_contraction_type is not None
        assert retrieved_contraction_type.id == contraction_type.id


class TestExerciseRelationships:
    """Test suite for exercise relationships and complex operations."""

    def test_exercise_with_all_relations(
        self,
        db_session: Session,
        test_user: User,
        exercise_category: ExerciseCategory,
        movement_type: MovementType,
        muscle_group: MuscleGroup,
        equipment: Equipment,
        position: Position,
        contraction_type: ContractionType,
    ):
        """Test creating exercise with all possible relations."""
        exercise_data = ExerciseCreate(
            name="Complete Exercise",
            short_name="CE",
            description="Exercise with all relations",
            category_id=exercise_category.id,
            movement_type_id=movement_type.id,
            muscle_group_id=muscle_group.id,
            equipment_id=equipment.id,
            position_id=position.id,
            contraction_type_id=contraction_type.id,
            type="strength",
            crossfit_variant={"rounds": 3, "reps": 10},
        )

        created_exercise = exercise.create_with_relations(
            db_session, obj_in=exercise_data, coach_id=test_user.id
        )

        # Verify all relations are set
        retrieved_exercise = exercise.get_with_relations(
            db_session, id=created_exercise.id
        )

        assert retrieved_exercise.category is not None
        assert retrieved_exercise.category.name == "Strength"
        assert retrieved_exercise.movement_type is not None
        assert retrieved_exercise.movement_type.name == "Compound"
        assert retrieved_exercise.muscle_group is not None
        assert retrieved_exercise.muscle_group.name == "Chest"
        assert retrieved_exercise.equipment is not None
        assert retrieved_exercise.equipment.name == "Barbell"
        assert retrieved_exercise.position is not None
        assert retrieved_exercise.position.name == "Standing"
        assert retrieved_exercise.contraction_type is not None
        assert retrieved_exercise.contraction_type.name == "Concentric"

    def test_get_multi_with_filters(
        self,
        db_session: Session,
        test_user: User,
        exercise_category: ExerciseCategory,
        muscle_group: MuscleGroup,
        equipment: Equipment,
    ):
        """Test getting exercises with multiple filters."""
        # Create exercises with different attributes
        exercise_data1 = ExerciseCreate(
            name="Exercise 1",
            category_id=exercise_category.id,
            muscle_group_id=muscle_group.id,
            equipment_id=equipment.id,
        )
        exercise_data2 = ExerciseCreate(
            name="Exercise 2",
            category_id=exercise_category.id,
            muscle_group_id=muscle_group.id,
        )

        exercise.create_with_relations(
            db_session, obj_in=exercise_data1, coach_id=test_user.id
        )
        exercise.create_with_relations(
            db_session, obj_in=exercise_data2, coach_id=test_user.id
        )

        # Filter by equipment
        exercises_with_equipment = exercise.get_multi_with_relations(
            db_session, equipment_id=equipment.id
        )
        assert len(exercises_with_equipment) == 1

        # Filter by category
        exercises_with_category = exercise.get_multi_with_relations(
            db_session, category_id=exercise_category.id
        )
        assert len(exercises_with_category) == 2

    def test_exercise_partial_update(
        self, db_session: Session, test_exercise: Exercise
    ):
        """Test partial update of exercise."""
        original_name = test_exercise.name
        update_data = ExerciseUpdate(description="Updated description only")

        updated_exercise = exercise.update(
            db_session, db_obj=test_exercise, obj_in=update_data
        )

        # Name should remain unchanged
        assert updated_exercise.name == original_name
        assert updated_exercise.description == "Updated description only"
