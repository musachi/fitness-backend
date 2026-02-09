from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from src.models.exercise import (
    ContractionType,
    Equipment,
    Exercise,
    ExerciseCategory,
    MovementType,
    MuscleGroup,
    Position,
)

# En src/crud/exercise.py, cambia esta línea:
from src.schemas.exercise import (
    ContractionTypeCreate,
    ContractionTypeUpdate,
    EquipmentCreate,
    EquipmentUpdate,
    ExerciseCategoryCreate,
    ExerciseCategoryUpdate,
    ExerciseCreate,
    ExerciseUpdate,
    MovementTypeCreate,
    MovementTypeUpdate,
    MuscleGroupCreate,
    MuscleGroupUpdate,
    PositionCreate,
    PositionUpdate,
)

from .base import CRUDBase


# CRUD for ExerciseCategory
class CRUDExerciseCategory(
    CRUDBase[ExerciseCategory, ExerciseCategoryCreate, ExerciseCategoryUpdate]
):
    def get_by_name(self, db: Session, *, name: str) -> ExerciseCategory | None:
        """Get category by name"""
        return db.query(ExerciseCategory).filter(ExerciseCategory.name == name).first()

    def get_with_displacement(self, db: Session) -> list[ExerciseCategory]:
        """Get categories with displacement"""
        return db.query(ExerciseCategory).filter(ExerciseCategory.displacement).all()


exercise_category = CRUDExerciseCategory(ExerciseCategory)


# CRUD for MovementType
class CRUDMovementType(CRUDBase[MovementType, MovementTypeCreate, MovementTypeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> MovementType | None:
        """Get movement type by name"""
        return db.query(MovementType).filter(MovementType.name == name).first()


movement_type = CRUDMovementType(MovementType)


# CRUD for MuscleGroup
class CRUDMuscleGroup(CRUDBase[MuscleGroup, MuscleGroupCreate, MuscleGroupUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> MuscleGroup | None:
        """Get muscle group by name"""
        return db.query(MuscleGroup).filter(MuscleGroup.name == name).first()


muscle_group = CRUDMuscleGroup(MuscleGroup)


# CRUD for Equipment
class CRUDEquipment(CRUDBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Equipment | None:
        """Get equipment by name"""
        return db.query(Equipment).filter(Equipment.name == name).first()


equipment = CRUDEquipment(Equipment)


# CRUD for Position
class CRUDPosition(CRUDBase[Position, PositionCreate, PositionUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Position | None:
        """Get position by name"""
        return db.query(Position).filter(Position.name == name).first()


position = CRUDPosition(Position)


# CRUD for ContractionType
class CRUDContractionType(
    CRUDBase[ContractionType, ContractionTypeCreate, ContractionTypeUpdate]
):
    def get_by_name(self, db: Session, *, name: str) -> ContractionType | None:
        """Get contraction type by name"""
        return db.query(ContractionType).filter(ContractionType.name == name).first()


contraction_type = CRUDContractionType(ContractionType)


# CRUD for Exercise
class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    def get_with_relations(self, db: Session, *, id: int) -> Exercise | None:
        """Get exercise with all relations"""
        return (
            db.query(Exercise)
            .options(
                joinedload(Exercise.category),
                joinedload(Exercise.movement_type),
                joinedload(Exercise.muscle_group),
                joinedload(Exercise.equipment),
                joinedload(Exercise.position),
                joinedload(Exercise.contraction_type),
                joinedload(Exercise.coach_user),
            )
            .filter(Exercise.id == id)
            .first()
        )

    def get_multi_with_relations(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        coach_id: UUID | None = None,
        category_id: int | None = None,
        muscle_group_id: int | None = None,
        equipment_id: int | None = None,
    ) -> list[Exercise]:
        """Get exercises with relations and optional filters"""
        query = db.query(Exercise).options(
            joinedload(Exercise.category),
            joinedload(Exercise.muscle_group),
            joinedload(Exercise.equipment),
            joinedload(Exercise.coach_user),
        )

        # Apply filters
        if coach_id:
            query = query.filter(Exercise.coach_id == coach_id)
        if category_id:
            query = query.filter(Exercise.category_id == category_id)
        if muscle_group_id:
            query = query.filter(Exercise.muscle_group_id == muscle_group_id)
        if equipment_id:
            query = query.filter(Exercise.equipment_id == equipment_id)

        return query.offset(skip).limit(limit).all()

    def search_exercises(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> list[Exercise]:
        """Search exercises by name or description"""
        return (
            db.query(Exercise)
            .filter(
                or_(
                    Exercise.name.ilike(f"%{query}%"),
                    Exercise.short_name.ilike(f"%{query}%"),
                    Exercise.description.ilike(f"%{query}%"),
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_coach(
        self, db: Session, *, coach_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Exercise]:
        """Get exercises created by a specific coach"""
        return (
            db.query(Exercise)
            .filter(Exercise.coach_id == coach_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_exercises_by_ids(self, db: Session, *, ids: list[int]) -> list[Exercise]:
        """Get multiple exercises by IDs"""
        return db.query(Exercise).filter(Exercise.id.in_(ids)).all()

    def create_with_relations(
        self, db: Session, *, obj_in: ExerciseCreate, coach_id: UUID
    ) -> Exercise:
        """Create exercise with coach ID"""
        exercise_data = obj_in.dict()
        exercise_data["coach_id"] = coach_id
        return self.create(db, obj_in=ExerciseCreate(**exercise_data))


exercise = CRUDExercise(Exercise)
