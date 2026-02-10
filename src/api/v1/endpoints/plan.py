from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.crud.plan import plan, workout_session, workout_exercise
from src.schemas.common import SuccessResponse
from src.schemas.plan import (
    PlanCreate, PlanUpdate, PlanResponse, PlansList,
    WorkoutSessionCreate, WorkoutSessionUpdate, WorkoutSessionResponse, WorkoutSessionsList,
    WorkoutExerciseResponse, WorkoutExercisesList,
    PlanTemplate, PlanFromTemplateRequest, PlanFromTemplateResponse
)
from src.services.plan_generator import PlanGenerator
from src.api.deps import get_current_active_user, get_current_coach_or_admin
from src.models.user import User

router = APIRouter()


# Plan endpoints
@router.get(
    "/",
    response_model=SuccessResponse,
    summary="Get workout plans",
    description="Retrieve workout plans with optional filters for pagination and user access.",
    responses={
        200: {
            "description": "Plans retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Plans retrieved successfully",
                        "data": {
                            "plans": [
                                {
                                    "id": 1,
                                    "name": "Beginner Full Body",
                                    "duration_weeks": 4,
                                    "coach_id": "uuid",
                                    "created_at": "2024-01-01T00:00:00",
                                    "updated_at": "2024-01-01T00:00:00",
                                    "workout_sessions": []
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
)
async def get_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    coach_id: Optional[str] = Query(None),
    is_public: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get workout plans with optional filters.

    Parameters:
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **coach_id**: Filter by coach ID
    - **is_public**: Filter by public status

    Returns:
    - List of workout plans
    """
    plans = plan(db).get_multi(
        skip=skip,
        limit=limit,
        coach_id=coach_id,
        is_public=is_public
    )

    return SuccessResponse(
        message="Plans retrieved successfully",
        data={"plans": [PlanResponse.from_orm(p) for p in plans]}
    )


@router.get("/my-plans", response_model=SuccessResponse)
async def get_my_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's workout plans.

    Returns:
    - List of user's workout plans
    """
    user_plans = plan(db).get_by_user(
        user_id=str(current_user.id),
        skip=skip,
        limit=limit
    )

    return SuccessResponse(
        message="User plans retrieved successfully",
        data={"plans": [PlanResponse.from_orm(p) for p in user_plans]}
    )


@router.get("/public", response_model=SuccessResponse)
async def get_public_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get public workout plans.

    Returns:
    - List of public workout plans
    """
    public_plans = plan(db).get_public_plans(skip=skip, limit=limit)

    return SuccessResponse(
        message="Public plans retrieved successfully",
        data={"plans": [PlanResponse.from_orm(p) for p in public_plans]}
    )


@router.get("/{plan_id}", response_model=SuccessResponse)
async def get_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific workout plan by ID.

    Parameters:
    - **plan_id**: ID of the plan to retrieve

    Returns:
    - Workout plan details
    """
    plan_obj = plan(db).get(plan_id)
    if not plan_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    return SuccessResponse(
        message="Plan retrieved successfully",
        data={"plan": PlanResponse.from_orm(plan_obj)}
    )


@router.post("/", response_model=SuccessResponse)
async def create_plan(
    plan_data: PlanCreate,
    current_user: User = Depends(get_current_coach_or_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new workout plan.

    Parameters:
    - **plan_data**: Plan creation data

    Returns:
    - Created plan details
    """
    new_plan = plan(db).create(plan_data, coach_id=str(current_user.id))

    return SuccessResponse(
        message="Plan created successfully",
        data={"plan": PlanResponse.from_orm(new_plan)}
    )


@router.put("/{plan_id}", response_model=SuccessResponse)
async def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a workout plan.

    Parameters:
    - **plan_id**: ID of the plan to update
    - **plan_data**: Plan update data

    Returns:
    - Updated plan details
    """
    # Check if plan exists and user owns it
    existing_plan = plan(db).get(plan_id)
    if not existing_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    if str(existing_plan.coach_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this plan"
        )

    updated_plan = plan(db).update(plan_id, plan_data)

    return SuccessResponse(
        message="Plan updated successfully",
        data={"plan": PlanResponse.from_orm(updated_plan)}
    )


@router.delete("/{plan_id}", response_model=SuccessResponse)
async def delete_plan(
    plan_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a workout plan.

    Parameters:
    - **plan_id**: ID of the plan to delete

    Returns:
    - Deletion confirmation
    """
    # Check if plan exists and user owns it
    existing_plan = plan(db).get(plan_id)
    if not existing_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    if str(existing_plan.coach_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this plan"
        )

    success = plan(db).delete(plan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete plan"
        )

    return SuccessResponse(
        message="Plan deleted successfully",
        data={"deleted": True}
    )


# Template endpoints
@router.get("/templates/available", response_model=SuccessResponse)
async def get_available_templates(db: Session = Depends(get_db)):
    """
    Get available workout plan templates.

    Returns:
    - List of plan templates with metadata
    """
    generator = PlanGenerator(db)
    templates = generator.get_available_templates()

    return SuccessResponse(
        message="Templates retrieved successfully",
        data={"templates": templates}
    )


@router.post("/generate-from-template", response_model=SuccessResponse)
async def generate_plan_from_template(
    request: PlanFromTemplateRequest,
    current_user: User = Depends(get_current_coach_or_admin),
    db: Session = Depends(get_db)
):
    """
    Generate a workout plan from a template.

    Parameters:
    - **template_name**: Name of template to use
    - **custom_name**: Optional custom name for the plan

    Returns:
    - Generated plan details
    """
    generator = PlanGenerator(db)

    try:
        generated_plan = generator.generate_plan_from_template(
            template_name=request.template_name,
            user_id=str(current_user.id),
            custom_name=request.custom_name
        )

        # Count generated workout sessions
        session_count = len(generated_plan.workout_sessions)

        return SuccessResponse(
            message="Plan generated successfully",
            data={
                "plan_id": generated_plan.id,
                "name": generated_plan.name,
                "duration_weeks": generated_plan.duration_weeks,
                "workouts_count": session_count
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate plan: {str(e)}"
        )


# Workout Session endpoints
@router.get("/{plan_id}/sessions", response_model=SuccessResponse)
async def get_plan_sessions(
    plan_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get workout sessions for a specific plan.

    Parameters:
    - **plan_id**: ID of the plan
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return

    Returns:
    - List of workout sessions
    """
    sessions = workout_session(db).get_by_plan(plan_id, skip=skip, limit=limit)

    return SuccessResponse(
        message="Workout sessions retrieved successfully",
        data={"sessions": [WorkoutSessionResponse.from_orm(s) for s in sessions]}
    )


@router.get("/sessions/{session_id}", response_model=SuccessResponse)
async def get_workout_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific workout session.

    Parameters:
    - **session_id**: ID of the workout session

    Returns:
    - Workout session details with exercises
    """
    session = workout_session(db).get(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout session not found"
        )

    return SuccessResponse(
        message="Workout session retrieved successfully",
        data={"session": WorkoutSessionResponse.from_orm(session)}
    )


@router.post("/sessions", response_model=SuccessResponse)
async def create_workout_session(
    session_data: WorkoutSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new workout session.

    Parameters:
    - **session_data**: Workout session creation data

    Returns:
    - Created workout session
    """
    # Verify user owns the plan
    plan_obj = plan(db).get(session_data.plan_id)
    if not plan_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )

    new_session = workout_session(db).create(session_data)

    return SuccessResponse(
        message="Workout session created successfully",
        data={"session": WorkoutSessionResponse.from_orm(new_session)}
    )


@router.put("/sessions/{session_id}/complete", response_model=SuccessResponse)
async def complete_workout_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Mark a workout session as completed.

    Parameters:
    - **session_id**: ID of the workout session

    Returns:
    - Updated workout session
    """
    completed_session = workout_session(db).mark_completed(session_id)
    if not completed_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout session not found"
        )

    return SuccessResponse(
        message="Workout session completed successfully",
        data={"session": WorkoutSessionResponse.from_orm(completed_session)}
    )
