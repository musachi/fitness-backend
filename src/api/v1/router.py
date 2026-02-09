from fastapi import APIRouter

from src.api.v1.endpoints import auth, exercise, health, user

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(exercise.router, prefix="/exercises", tags=["exercises"])

api_router.include_router(health.router, tags=["health"])
