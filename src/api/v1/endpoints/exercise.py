from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.deps import get_current_coach
from src.core.database import get_db
from src.crud.exercise import (
    contraction_type,
    equipment,
    exercise,
    exercise_category,
    movement_type,
    muscle_group,
    position,
)
from src.schemas.exercise import (
    ContractionType,
    ContractionTypeCreate,
    ContractionTypesList,
    ContractionTypeUpdate,
    Equipment,
    EquipmentCreate,
    EquipmentList,
    EquipmentUpdate,
    Exercise,
    ExerciseCategoriesList,
    ExerciseCategory,
    ExerciseCategoryCreate,
    ExerciseCategoryUpdate,
    ExerciseCreate,
    ExerciseList,
    ExerciseUpdate,
    MovementType,
    MovementTypeCreate,
    MovementTypesList,
    MovementTypeUpdate,
    MuscleGroup,
    MuscleGroupCreate,
    MuscleGroupsList,
    MuscleGroupUpdate,
    Position,
    PositionCreate,
    PositionsList,
    PositionUpdate,
)

router = APIRouter(tags=["exercises"])


# Exercise endpoints
@router.get("/", response_model=ExerciseList)
async def read_exercises(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    coach_id: UUID | None = None,
    category_id: int | None = None,
    muscle_group_id: int | None = None,
    equipment_id: int | None = None,
    search: str | None = None,
):
    """
    Retrieve exercises with optional filters
    """
    if search:
        exercises_list = exercise.search_exercises(
            db, query=search, skip=skip, limit=limit
        )
        total = len(exercises_list)  # Simplified, should count separately
    else:
        exercises_list = exercise.get_multi_with_relations(
            db,
            skip=skip,
            limit=limit,
            coach_id=coach_id,
            category_id=category_id,
            muscle_group_id=muscle_group_id,
            equipment_id=equipment_id,
        )
        total = exercise.count(db)

    return ExerciseList(
        exercises=exercises_list,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=limit,
    )


@router.get("/{exercise_id}", response_model=Exercise)
async def read_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Get exercise by ID with all relations
    """
    exercise_obj = exercise.get_with_relations(db, id=exercise_id)
    if not exercise_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    return exercise_obj


@router.post("/", response_model=Exercise, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise_in: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),  # Only coaches can create
):
    """
    Create new exercise
    """
    created_exercise = exercise.create_with_relations(
        db, obj_in=exercise_in, coach_id=current_user.id
    )
    return created_exercise


@router.put("/{exercise_id}", response_model=Exercise)
async def update_exercise(
    exercise_id: int,
    exercise_in: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    """
    Update exercise (only creator or admin can update)
    """
    exercise_obj = exercise.get(db, id=exercise_id)
    if not exercise_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    # Check permissions: creator or admin
    if exercise_obj.coach_id != current_user.id and current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    updated_exercise = exercise.update(db, db_obj=exercise_obj, obj_in=exercise_in)
    return updated_exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    """
    Delete exercise (only creator or admin can delete)
    """
    exercise_obj = exercise.get(db, id=exercise_id)
    if not exercise_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    # Check permissions: creator or admin
    if exercise_obj.coach_id != current_user.id and current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    exercise.remove(db, id=exercise_id)
    return None


# Classification endpoints (Exercise Categories)
@router.get("/categories/", response_model=ExerciseCategoriesList)
async def read_categories(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get all exercise categories
    """
    categories = exercise_category.get_multi(db, skip=skip, limit=limit)
    total = exercise_category.count(db)

    return ExerciseCategoriesList(categories=categories, total=total)


@router.get("/categories/{category_id}", response_model=ExerciseCategory)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get exercise category by ID
    """
    category = exercise_category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return category


@router.post(
    "/categories/", response_model=ExerciseCategory, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_in: ExerciseCategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),  # Only coaches can create
):
    """
    Create new exercise category
    """
    # Check if category with same name exists
    existing = exercise_category.get_by_name(db, name=category_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    created_category = exercise_category.create(db, obj_in=category_in)
    return created_category


@router.put("/categories/{category_id}", response_model=ExerciseCategory)
async def update_category(
    category_id: int,
    category_in: ExerciseCategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    """
    Update exercise category
    """
    category_obj = exercise_category.get(db, id=category_id)
    if not category_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Check if name conflicts with existing category
    if category_in.name and category_in.name != category_obj.name:
        existing = exercise_category.get_by_name(db, name=category_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists",
            )

    return exercise_category.update(db, db_obj=category_obj, obj_in=category_in)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    """
    Delete exercise category
    """
    category_obj = exercise_category.get(db, id=category_id)
    if not category_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    exercise_category.remove(db, id=category_id)
    return None


# Movement Types - Complete CRUD
@router.get("/movement-types/", response_model=MovementTypesList)
async def read_movement_types(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    movement_types_list = movement_type.get_multi(db, skip=skip, limit=limit)
    total = movement_type.count(db)
    return MovementTypesList(movement_types=movement_types_list, total=total)


@router.get("/movement-types/{movement_type_id}", response_model=MovementType)
async def read_movement_type(movement_type_id: int, db: Session = Depends(get_db)):
    movement_type_obj = movement_type.get(db, id=movement_type_id)
    if not movement_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movement type not found"
        )
    return movement_type_obj


@router.post(
    "/movement-types/", response_model=MovementType, status_code=status.HTTP_201_CREATED
)
async def create_movement_type(
    movement_type_in: MovementTypeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    existing = movement_type.get_by_name(db, name=movement_type_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movement type with this name already exists",
        )
    return movement_type.create(db, obj_in=movement_type_in)


@router.put("/movement-types/{movement_type_id}", response_model=MovementType)
async def update_movement_type(
    movement_type_id: int,
    movement_type_in: MovementTypeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    movement_type_obj = movement_type.get(db, id=movement_type_id)
    if not movement_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movement type not found"
        )
    return movement_type.update(db, db_obj=movement_type_obj, obj_in=movement_type_in)


@router.delete(
    "/movement-types/{movement_type_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_movement_type(
    movement_type_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    movement_type_obj = movement_type.get(db, id=movement_type_id)
    if not movement_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movement type not found"
        )
    movement_type.remove(db, id=movement_type_id)
    return None


# Muscle Groups - Complete CRUD
@router.get("/muscle-groups/", response_model=MuscleGroupsList)
async def read_muscle_groups(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    muscle_groups_list = muscle_group.get_multi(db, skip=skip, limit=limit)
    total = muscle_group.count(db)
    return MuscleGroupsList(muscle_groups=muscle_groups_list, total=total)


@router.get("/muscle-groups/{muscle_group_id}", response_model=MuscleGroup)
async def read_muscle_group(muscle_group_id: int, db: Session = Depends(get_db)):
    muscle_group_obj = muscle_group.get(db, id=muscle_group_id)
    if not muscle_group_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Muscle group not found"
        )
    return muscle_group_obj


@router.post(
    "/muscle-groups/", response_model=MuscleGroup, status_code=status.HTTP_201_CREATED
)
async def create_muscle_group(
    muscle_group_in: MuscleGroupCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    existing = muscle_group.get_by_name(db, name=muscle_group_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Muscle group with this name already exists",
        )
    return muscle_group.create(db, obj_in=muscle_group_in)


@router.put("/muscle-groups/{muscle_group_id}", response_model=MuscleGroup)
async def update_muscle_group(
    muscle_group_id: int,
    muscle_group_in: MuscleGroupUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    muscle_group_obj = muscle_group.get(db, id=muscle_group_id)
    if not muscle_group_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Muscle group not found"
        )

    # Check if name conflicts with existing muscle group
    if muscle_group_in.name and muscle_group_in.name != muscle_group_obj.name:
        existing = muscle_group.get_by_name(db, name=muscle_group_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Muscle group with this name already exists",
            )

    return muscle_group.update(db, db_obj=muscle_group_obj, obj_in=muscle_group_in)


@router.delete(
    "/muscle-groups/{muscle_group_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_muscle_group(
    muscle_group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    muscle_group_obj = muscle_group.get(db, id=muscle_group_id)
    if not muscle_group_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Muscle group not found"
        )
    muscle_group.remove(db, id=muscle_group_id)
    return None


# Equipment - Complete CRUD
@router.get("/equipment/", response_model=EquipmentList)
async def read_equipment(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    equipment_list = equipment.get_multi(db, skip=skip, limit=limit)
    total = equipment.count(db)
    return EquipmentList(equipment=equipment_list, total=total)


@router.get("/equipment/{equipment_id}", response_model=Equipment)
async def read_equipment_item(equipment_id: int, db: Session = Depends(get_db)):
    equipment_obj = equipment.get(db, id=equipment_id)
    if not equipment_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )
    return equipment_obj


@router.post(
    "/equipment/", response_model=Equipment, status_code=status.HTTP_201_CREATED
)
async def create_equipment(
    equipment_in: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    existing = equipment.get_by_name(db, name=equipment_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Equipment with this name already exists",
        )
    return equipment.create(db, obj_in=equipment_in)


@router.put("/equipment/{equipment_id}", response_model=Equipment)
async def update_equipment(
    equipment_id: int,
    equipment_in: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    equipment_obj = equipment.get(db, id=equipment_id)
    if not equipment_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    # Check if name conflicts with existing equipment
    if equipment_in.name and equipment_in.name != equipment_obj.name:
        existing = equipment.get_by_name(db, name=equipment_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Equipment with this name already exists",
            )

    return equipment.update(db, db_obj=equipment_obj, obj_in=equipment_in)


@router.delete("/equipment/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    equipment_obj = equipment.get(db, id=equipment_id)
    if not equipment_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )
    equipment.remove(db, id=equipment_id)
    return None


# Positions - Complete CRUD
@router.get("/positions/", response_model=PositionsList)
async def read_positions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    positions_list = position.get_multi(db, skip=skip, limit=limit)
    total = position.count(db)
    return PositionsList(positions=positions_list, total=total)


@router.get("/positions/{position_id}", response_model=Position)
async def read_position(position_id: int, db: Session = Depends(get_db)):
    position_obj = position.get(db, id=position_id)
    if not position_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    return position_obj


@router.post(
    "/positions/", response_model=Position, status_code=status.HTTP_201_CREATED
)
async def create_position(
    position_in: PositionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    existing = position.get_by_name(db, name=position_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position with this name already exists",
        )
    return position.create(db, obj_in=position_in)


@router.put("/positions/{position_id}", response_model=Position)
async def update_position(
    position_id: int,
    position_in: PositionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    position_obj = position.get(db, id=position_id)
    if not position_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )

    # Check if name conflicts with existing position
    if position_in.name and position_in.name != position_obj.name:
        existing = position.get_by_name(db, name=position_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Position with this name already exists",
            )

    return position.update(db, db_obj=position_obj, obj_in=position_in)


@router.delete("/positions/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    position_obj = position.get(db, id=position_id)
    if not position_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    position.remove(db, id=position_id)
    return None


# Contraction Types - Complete CRUD
@router.get("/contraction-types/", response_model=ContractionTypesList)
async def read_contraction_types(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    contraction_types_list = contraction_type.get_multi(db, skip=skip, limit=limit)
    total = contraction_type.count(db)
    return ContractionTypesList(contraction_types=contraction_types_list, total=total)


@router.get("/contraction-types/{contraction_type_id}", response_model=ContractionType)
async def read_contraction_type(
    contraction_type_id: int, db: Session = Depends(get_db)
):
    contraction_type_obj = contraction_type.get(db, id=contraction_type_id)
    if not contraction_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contraction type not found"
        )
    return contraction_type_obj


@router.post(
    "/contraction-types/",
    response_model=ContractionType,
    status_code=status.HTTP_201_CREATED,
)
async def create_contraction_type(
    contraction_type_in: ContractionTypeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    existing = contraction_type.get_by_name(db, name=contraction_type_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraction type with this name already exists",
        )
    return contraction_type.create(db, obj_in=contraction_type_in)


@router.put("/contraction-types/{contraction_type_id}", response_model=ContractionType)
async def update_contraction_type(
    contraction_type_id: int,
    contraction_type_in: ContractionTypeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    contraction_type_obj = contraction_type.get(db, id=contraction_type_id)
    if not contraction_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contraction type not found"
        )

    # Check if name conflicts with existing contraction type
    if (
        contraction_type_in.name
        and contraction_type_in.name != contraction_type_obj.name
    ):
        existing = contraction_type.get_by_name(db, name=contraction_type_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraction type with this name already exists",
            )

    return contraction_type.update(
        db, db_obj=contraction_type_obj, obj_in=contraction_type_in
    )


@router.delete(
    "/contraction-types/{contraction_type_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_contraction_type(
    contraction_type_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
):
    contraction_type_obj = contraction_type.get(db, id=contraction_type_id)
    if not contraction_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contraction type not found"
        )
    contraction_type.remove(db, id=contraction_type_id)
    return None


# Get exercises by coach
@router.get("/coach/mine", response_model=ExerciseList)
async def read_my_exercises(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_coach),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get exercises created by current coach
    """
    exercises_list = exercise.get_by_coach(
        db, coach_id=current_user.id, skip=skip, limit=limit
    )
    total = len(exercises_list)  # Should count separately

    return ExerciseList(
        exercises=exercises_list,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=limit,
    )
