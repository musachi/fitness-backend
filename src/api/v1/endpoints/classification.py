from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_current_admin
from src.crud.classification import classification_type, classification_value
from src.schemas.classification import (
    ClassificationType as ClassificationTypeSchema,
    ClassificationTypeCreate,
    ClassificationTypeUpdate,
    ClassificationValue as ClassificationValueSchema,
    ClassificationValueCreate,
    ClassificationValueUpdate,
    ClassificationTypeWithValues
)
from src.models.user import User

router = APIRouter()


# ================================
# CLASSIFICATION TYPES ENDPOINTS
# ================================

@router.get("/classification-types", response_model=List[ClassificationTypeSchema])
def get_classification_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    applies_to: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all classification types with optional filtering and pagination.
    """
    types, _ = classification_type.get_multi(
        db=db, 
        skip=skip, 
        limit=limit,
        search=search,
        applies_to=applies_to
    )
    
    # Add value count for each type
    result = []
    for type_obj in types:
        type_dict = {
            "id": type_obj.id,
            "name": type_obj.name,
            "description": type_obj.description,
            "applies_to": type_obj.applies_to,
            "is_required": type_obj.is_required,
            "created_at": type_obj.created_at,
            "updated_at": type_obj.updated_at,
            "value_count": len(type_obj.classification_values)
        }
        result.append(ClassificationTypeSchema(**type_dict))
    
    return result


@router.post("/classification-types", response_model=ClassificationTypeSchema)
def create_classification_type(
    *,
    db: Session = Depends(get_db),
    classification_type_in: ClassificationTypeCreate,
    current_user: User = Depends(get_current_admin)
):
    """
    Create new classification type. Admin only.
    """
    # Check if name already exists
    existing = classification_type.get_by_name(db, name=classification_type_in.name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Classification type with name '{classification_type_in.name}' already exists"
        )
    
    return classification_type.create(db=db, obj_in=classification_type_in)


@router.get("/classification-types/{type_id}", response_model=ClassificationTypeWithValues)
def get_classification_type(
    type_id: int,
    db: Session = Depends(get_db)
):
    """
    Get classification type by ID with its values.
    """
    type_obj = classification_type.get(db=db, id=type_id)
    if not type_obj:
        raise HTTPException(status_code=404, detail="Classification type not found")
    
    return type_obj


@router.put("/classification-types/{type_id}", response_model=ClassificationTypeSchema)
def update_classification_type(
    *,
    db: Session = Depends(get_db),
    type_id: int,
    classification_type_in: ClassificationTypeUpdate,
    current_user: User = Depends(get_current_admin)
):
    """
    Update classification type. Admin only.
    """
    type_obj = classification_type.get(db=db, id=type_id)
    if not type_obj:
        raise HTTPException(status_code=404, detail="Classification type not found")
    
    # Check if name already exists (if updating name)
    if classification_type_in.name and classification_type_in.name != type_obj.name:
        existing = classification_type.get_by_name(db, name=classification_type_in.name)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Classification type with name '{classification_type_in.name}' already exists"
            )
    
    return classification_type.update(db=db, db_obj=type_obj, obj_in=classification_type_in)


@router.delete("/classification-types/{type_id}")
def delete_classification_type(
    *,
    db: Session = Depends(get_db),
    type_id: int,
    current_user: User = Depends(get_current_admin)
):
    """
    Delete classification type. Admin only.
    """
    type_obj = classification_type.get(db=db, id=type_id)
    if not type_obj:
        raise HTTPException(status_code=404, detail="Classification type not found")
    
    classification_type.delete(db=db, id=type_id)
    return {"message": "Classification type deleted successfully"}


# ================================
# CLASSIFICATION VALUES ENDPOINTS
# ================================

@router.get("/classification-values", response_model=List[ClassificationValueSchema])
def get_classification_values(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    classification_type_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all classification values with optional filtering and pagination.
    """
    values, _ = classification_value.get_multi(
        db=db, 
        skip=skip, 
        limit=limit,
        search=search,
        classification_type_id=classification_type_id
    )
    return values


@router.post("/classification-values", response_model=ClassificationValueSchema)
def create_classification_value(
    *,
    db: Session = Depends(get_db),
    classification_value_in: ClassificationValueCreate,
    current_user: User = Depends(get_current_admin)
):
    """
    Create new classification value. Admin only.
    """
    # Check if classification type exists
    type_obj = classification_type.get(db=db, id=classification_value_in.classification_type_id)
    if not type_obj:
        raise HTTPException(status_code=404, detail="Classification type not found")
    
    # Check if value already exists for this type
    existing = classification_value.get_by_type_and_value(
        db, 
        classification_type_id=classification_value_in.classification_type_id,
        value=classification_value_in.value
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Value '{classification_value_in.value}' already exists for this classification type"
        )
    
    # Auto-set order if not provided
    if classification_value_in.order == 0:
        max_order = classification_value.get_max_order(db, classification_value_in.classification_type_id)
        classification_value_in.order = max_order + 1
    
    return classification_value.create(db=db, obj_in=classification_value_in)


@router.get("/classification-values/{value_id}", response_model=ClassificationValueSchema)
def get_classification_value(
    value_id: int,
    db: Session = Depends(get_db)
):
    """
    Get classification value by ID.
    """
    value_obj = classification_value.get(db=db, id=value_id)
    if not value_obj:
        raise HTTPException(status_code=404, detail="Classification value not found")
    
    return value_obj


@router.put("/classification-values/{value_id}", response_model=ClassificationValueSchema)
def update_classification_value(
    *,
    db: Session = Depends(get_db),
    value_id: int,
    classification_value_in: ClassificationValueUpdate,
    current_user: User = Depends(get_current_admin)
):
    """
    Update classification value. Admin only.
    """
    value_obj = classification_value.get(db=db, id=value_id)
    if not value_obj:
        raise HTTPException(status_code=404, detail="Classification value not found")
    
    # Check if value already exists for this type (if updating value)
    if classification_value_in.value and classification_value_in.value != value_obj.value:
        existing = classification_value.get_by_type_and_value(
            db, 
            classification_type_id=value_obj.classification_type_id,
            value=classification_value_in.value
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Value '{classification_value_in.value}' already exists for this classification type"
            )
    
    return classification_value.update(db=db, db_obj=value_obj, obj_in=classification_value_in)


@router.delete("/classification-values/{value_id}")
def delete_classification_value(
    *,
    db: Session = Depends(get_db),
    value_id: int,
    current_user: User = Depends(get_current_admin)
):
    """
    Delete classification value. Admin only.
    """
    value_obj = classification_value.get(db=db, id=value_id)
    if not value_obj:
        raise HTTPException(status_code=404, detail="Classification value not found")
    
    classification_value.delete(db=db, id=value_id)
    return {"message": "Classification value deleted successfully"}
