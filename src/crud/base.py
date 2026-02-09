from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        Base CRUD class with default methods
        """
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        """Get by ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order_direction: str = "asc",
    ) -> list[ModelType]:
        """Get multiple records with pagination"""
        query = db.query(self.model)

        if order_by:
            column = getattr(self.model, order_by, None)
            if column:
                if order_direction.lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create new record"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Update existing record"""
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        """Delete record"""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def count(self, db: Session) -> int:
        """Count total records"""
        return db.query(self.model).count()

    def exists(self, db: Session, *, id: Any) -> bool:
        """Check if record exists"""
        return db.query(self.model).filter(self.model.id == id).first() is not None

    def search(
        self, db: Session, *, field: str, value: Any, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """Search records by field value"""
        column = getattr(self.model, field, None)
        if not column:
            return []

        return (
            db.query(self.model)
            .filter(column.ilike(f"%{value}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
