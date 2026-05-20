from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    DataIntegrityError,
    ErrorDetail,
    SaratealError,
    ValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(SaratealError)
    async def handle_sarateal_error(
        request: Request,
        exc: SaratealError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_response(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details: list[ErrorDetail] = []

        for error in exc.errors():
            location = error.get("loc", [])
            field = ".".join(str(part) for part in location if part != "body")

            details.append(
                ErrorDetail(
                    field=field or None,
                    message=str(error.get("msg", "Invalid value.")),
                    value=error.get("input"),
                )
            )

        validation_error = ValidationError(
            message="Request validation failed.",
            details=details,
            context={
                "path": str(request.url.path),
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=validation_error.status_code,
            content=validation_error.to_response(),
        )

    @app.exception_handler(IntegrityError)
    async def handle_database_integrity_error(
        request: Request,
        exc: IntegrityError,
    ) -> JSONResponse:
        integrity_error = DataIntegrityError(
            message="Database integrity constraint failed.",
            context={
                "path": str(request.url.path),
                "method": request.method,
                "reason": "A duplicate, missing reference, or invalid database relationship was detected.",
            },
        )

        return JSONResponse(
            status_code=integrity_error.status_code,
            content=integrity_error.to_response(),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        internal_error = SaratealError(
            message="An unexpected internal error occurred.",
            context={
                "path": str(request.url.path),
                "method": request.method,
                "error_type": exc.__class__.__name__,
            },
        )

        return JSONResponse(
            status_code=internal_error.status_code,
            content=internal_error.to_response(),
        )