from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette import status


class AppException(HTTPException):
    """Base application exception."""

    pass


class DatabaseException(AppException):
    """Database operation exception."""

    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(status_code=500, detail=detail)


class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class BadRequestException(AppException):
    """Bad request exception."""

    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)


class ValidationException(AppException):
    """Validation exception."""

    def __init__(self, detail: str = "Validation error", errors: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=422, detail=detail)
        self.errors = errors


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "status_code": exc.status_code,
            }
        },
    )


async def http_422_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation error",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "detail": exc.detail if hasattr(exc, "detail") else str(exc),
            }
        },
    )
