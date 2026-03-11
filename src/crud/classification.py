from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from src.models.classification import ClassificationType, ClassificationValue
from src.schemas.classification import (
    ClassificationTypeCreate, 
    ClassificationTypeUpdate,
    ClassificationValueCreate,
    ClassificationValueUpdate
)


# Classification Type CRUD
class ClassificationTypeCRUD:
    def get(self, db: Session, id: int) -> Optional[ClassificationType]:
        return db.query(ClassificationType).filter(ClassificationType.id == id).first()

    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        applies_to: Optional[str] = None
    ) -> tuple[List[ClassificationType], int]:
        query = db.query(ClassificationType)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    ClassificationType.name.ilike(f"%{search}%"),
                    ClassificationType.description.ilike(f"%{search}%")
                )
            )
        
        if applies_to:
            query = query.filter(ClassificationType.applies_to == applies_to)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        results = query.order_by(desc(ClassificationType.created_at)).offset(skip).limit(limit).all()
        
        return results, total

    def create(self, db: Session, obj_in: ClassificationTypeCreate) -> ClassificationType:
        db_obj = ClassificationType(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, 
        db: Session, 
        db_obj: ClassificationType, 
        obj_in: ClassificationTypeUpdate
    ) -> ClassificationType:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> ClassificationType:
        obj = db.query(ClassificationType).filter(ClassificationType.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_name(self, db: Session, name: str) -> Optional[ClassificationType]:
        return db.query(ClassificationType).filter(ClassificationType.name == name).first()


# Classification Value CRUD
class ClassificationValueCRUD:
    def get(self, db: Session, id: int) -> Optional[ClassificationValue]:
        return db.query(ClassificationValue).filter(ClassificationValue.id == id).first()

    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        classification_type_id: Optional[int] = None
    ) -> tuple[List[ClassificationValue], int]:
        query = db.query(ClassificationValue)
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    ClassificationValue.value.ilike(f"%{search}%"),
                    ClassificationValue.description.ilike(f"%{search}%")
                )
            )
        
        if classification_type_id:
            query = query.filter(ClassificationValue.classification_type_id == classification_type_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        results = query.order_by(
            ClassificationValue.classification_type_id,
            ClassificationValue.order,
            ClassificationValue.value
        ).offset(skip).limit(limit).all()
        
        return results, total

    def create(self, db: Session, obj_in: ClassificationValueCreate) -> ClassificationValue:
        db_obj = ClassificationValue(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, 
        db: Session, 
        db_obj: ClassificationValue, 
        obj_in: ClassificationValueUpdate
    ) -> ClassificationValue:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> ClassificationValue:
        obj = db.query(ClassificationValue).filter(ClassificationValue.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_type_and_value(
        self, 
        db: Session, 
        classification_type_id: int, 
        value: str
    ) -> Optional[ClassificationValue]:
        return db.query(ClassificationValue).filter(
            and_(
                ClassificationValue.classification_type_id == classification_type_id,
                ClassificationValue.value == value
            )
        ).first()

    def get_max_order(self, db: Session, classification_type_id: int) -> int:
        result = db.query(ClassificationValue).filter(
            ClassificationValue.classification_type_id == classification_type_id
        ).order_by(desc(ClassificationValue.order)).first()
        
        return result.order if result else -1


# Create instances
classification_type = ClassificationTypeCRUD()
classification_value = ClassificationValueCRUD()
