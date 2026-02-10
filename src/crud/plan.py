from __future__ import annotations

from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.models.plan import Plan, WorkoutExercise, WorkoutSession
from src.schemas.plan import (
    PlanCreate,
    PlanUpdate,
    WorkoutSessionCreate,
    WorkoutSessionUpdate,
)


class PlanCRUD:
    """CRUD operations for Plan model."""

    def __init__(self, db: Session):
        self.db = db

    def get(self, plan_id: int) -> Optional[Plan]:
        """Get plan by ID."""
        return self.db.query(Plan).filter(Plan.id == plan_id).first()

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        coach_id: Optional[str] = None,
        is_public: Optional[bool] = None
    ) -> list[Plan]:
        """Get multiple plans with optional filters."""
        query = self.db.query(Plan)

        if coach_id:
            query = query.filter(Plan.coach_id == coach_id)

        if is_public is not None:
            query = query.filter(Plan.is_public == is_public)

        return query.offset(skip).limit(limit).all()

    def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> list[Plan]:
        """Get plans created by a specific user."""
        return (
            self.db.query(Plan)
            .filter(Plan.coach_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_public_plans(self, skip: int = 0, limit: int = 100) -> list[Plan]:
        """Get public plans."""
        return (
            self.db.query(Plan)
            .filter(Plan.is_public == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, plan_data: PlanCreate, coach_id: str) -> Plan:
        """Create a new plan."""
        plan = Plan(
            name=plan_data.name,
            description=plan_data.description,
            duration_weeks=plan_data.duration_weeks,
            coach_id=coach_id
        )

        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def update(self, plan_id: int, plan_data: PlanUpdate) -> Optional[Plan]:
        """Update an existing plan."""
        plan = self.get(plan_id)
        if not plan:
            return None

        update_data = plan_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(plan, field, value)

        self.db.commit()
        self.db.refresh(plan)
        return plan

    def delete(self, plan_id: int) -> bool:
        """Delete a plan."""
        plan = self.get(plan_id)
        if not plan:
            return False

        self.db.delete(plan)
        self.db.commit()
        return True

    def count(self, coach_id: Optional[str] = None) -> int:
        """Count plans with optional filter."""
        query = self.db.query(Plan)

        if coach_id:
            query = query.filter(Plan.coach_id == coach_id)

        return query.count()


class WorkoutSessionCRUD:
    """CRUD operations for WorkoutSession model."""

    def __init__(self, db: Session):
        self.db = db

    def get(self, session_id: int) -> Optional[WorkoutSession]:
        """Get workout session by ID."""
        return (
            self.db.query(WorkoutSession)
            .filter(WorkoutSession.id == session_id)
            .first()
        )

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        plan_id: Optional[int] = None,
        client_id: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> list[WorkoutSession]:
        """Get multiple workout sessions with filters."""
        query = self.db.query(WorkoutSession)

        if plan_id:
            query = query.filter(WorkoutSession.plan_id == plan_id)

        if client_id:
            query = query.filter(WorkoutSession.client_id == client_id)

        if completed is not None:
            query = query.filter(WorkoutSession.completed == completed)

        return query.offset(skip).limit(limit).all()

    def get_by_plan(self, plan_id: int, skip: int = 0, limit: int = 100) -> list[WorkoutSession]:
        """Get workout sessions for a specific plan."""
        return (
            self.db.query(WorkoutSession)
            .filter(WorkoutSession.plan_id == plan_id)
            .order_by(WorkoutSession.date)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> list[WorkoutSession]:
        """Get workout sessions for a specific client."""
        return (
            self.db.query(WorkoutSession)
            .filter(WorkoutSession.client_id == client_id)
            .order_by(WorkoutSession.date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, session_data: WorkoutSessionCreate) -> WorkoutSession:
        """Create a new workout session."""
        session = WorkoutSession(
            plan_id=session_data.plan_id,
            client_id=session_data.client_id,
            date=session_data.date,
            notes=session_data.notes
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update(self, session_id: int, session_data: WorkoutSessionUpdate) -> Optional[WorkoutSession]:
        """Update an existing workout session."""
        session = self.get(session_id)
        if not session:
            return None

        update_data = session_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)

        self.db.commit()
        self.db.refresh(session)
        return session

    def mark_completed(self, session_id: int) -> Optional[WorkoutSession]:
        """Mark a workout session as completed."""
        session = self.get(session_id)
        if not session:
            return None

        session.completed = True
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, session_id: int) -> bool:
        """Delete a workout session."""
        session = self.get(session_id)
        if not session:
            return False

        self.db.delete(session)
        self.db.commit()
        return True


class WorkoutExerciseCRUD:
    """CRUD operations for WorkoutExercise model."""

    def __init__(self, db: Session):
        self.db = db

    def get(self, exercise_id: int) -> Optional[WorkoutExercise]:
        """Get workout exercise by ID."""
        return (
            self.db.query(WorkoutExercise)
            .filter(WorkoutExercise.id == exercise_id)
            .first()
        )

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        session_id: Optional[int] = None,
        exercise_id: Optional[int] = None
    ) -> list[WorkoutExercise]:
        """Get multiple workout exercises with filters."""
        query = self.db.query(WorkoutExercise)

        if session_id:
            query = query.filter(WorkoutExercise.session_id == session_id)

        if exercise_id:
            query = query.filter(WorkoutExercise.exercise_id == exercise_id)

        return query.offset(skip).limit(limit).all()

    def get_by_session(self, session_id: int) -> list[WorkoutExercise]:
        """Get workout exercises for a specific session."""
        return (
            self.db.query(WorkoutExercise)
            .filter(WorkoutExercise.session_id == session_id)
            .order_by(WorkoutExercise.id)
            .all()
        )

    def create(
        self,
        session_id: int,
        exercise_id: int,
        sets_planned: int,
        reps_planned: str,
        weight_planned: Optional[str] = None,
        rest_between_sets: Optional[str] = None
    ) -> WorkoutExercise:
        """Create a new workout exercise."""
        workout_exercise = WorkoutExercise(
            session_id=session_id,
            exercise_id=exercise_id,
            sets_planned=sets_planned,
            reps_planned=reps_planned,
            weight_planned=weight_planned,
            rest_between_sets=rest_between_sets
        )

        self.db.add(workout_exercise)
        self.db.commit()
        self.db.refresh(workout_exercise)
        return workout_exercise

    def update_progress(
        self,
        exercise_id: int,
        sets_done: Optional[int] = None,
        reps_done: Optional[list[int]] = None,
        weight_used: Optional[str] = None,
        time_spent: Optional[str] = None
    ) -> Optional[WorkoutExercise]:
        """Update workout exercise progress."""
        exercise = self.get(exercise_id)
        if not exercise:
            return None

        if sets_done is not None:
            exercise.sets_done = sets_done

        if reps_done is not None:
            exercise.reps_done = reps_done

        if weight_used is not None:
            exercise.weight_used = weight_used

        if time_spent is not None:
            exercise.time_spent = time_spent

        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def delete(self, exercise_id: int) -> bool:
        """Delete a workout exercise."""
        exercise = self.get(exercise_id)
        if not exercise:
            return False

        self.db.delete(exercise)
        self.db.commit()
        return True


# Create instances
plan = PlanCRUD
workout_session = WorkoutSessionCRUD
workout_exercise = WorkoutExerciseCRUD
