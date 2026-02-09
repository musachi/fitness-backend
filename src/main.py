import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.router import api_router
from src.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix="/api/v1")


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Fitness App API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
