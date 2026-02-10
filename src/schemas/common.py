from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Standard success response schema."""
    message: str
    data: Optional[Any] = None
    status: str = "success"


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None
    status: str = "error"


class PaginatedResponse(BaseModel):
    """Paginated response schema."""
    items: list[Any]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    version: str
    timestamp: str
    database: str
    uptime: Optional[str] = None
