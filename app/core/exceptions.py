from dataclasses import dataclass
from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_RECORD = "DUPLICATE_RECORD"
    RECORD_NOT_FOUND = "RECORD_NOT_FOUND"
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    DATA_INTEGRITY_ERROR = "DATA_INTEGRITY_ERROR"
    EXTERNAL_SOURCE_ERROR = "EXTERNAL_SOURCE_ERROR"
    UNAUTHORIZED_ACTION = "UNAUTHORIZED_ACTION"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass(frozen=True)
class ErrorDetail:
    field: str | None
    message: str
    value: Any | None = None


class SaratealError(Exception):
    status_code: int = 500
    error_code: ErrorCode = ErrorCode.INTERNAL_ERROR

    def __init__(
        self,
        message: str,
        *,
        details: list[ErrorDetail] | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.details = details or []
        self.context = context or {}

        super().__init__(message)

    def to_response(self) -> dict[str, Any]:
        return {
            "error": {
                "code": self.error_code.value,
                "message": self.message,
                "details": [
                    {
                        "field": detail.field,
                        "message": detail.message,
                        "value": detail.value,
                    }
                    for detail in self.details
                ],
                "context": self.context,
            }
        }


class ValidationError(SaratealError):
    status_code = 422
    error_code = ErrorCode.VALIDATION_ERROR


class DuplicateRecordError(SaratealError):
    status_code = 409
    error_code = ErrorCode.DUPLICATE_RECORD


class RecordNotFoundError(SaratealError):
    status_code = 404
    error_code = ErrorCode.RECORD_NOT_FOUND


class BusinessRuleViolationError(SaratealError):
    status_code = 400
    error_code = ErrorCode.BUSINESS_RULE_VIOLATION


class DataIntegrityError(SaratealError):
    status_code = 409
    error_code = ErrorCode.DATA_INTEGRITY_ERROR


class ExternalSourceError(SaratealError):
    status_code = 502
    error_code = ErrorCode.EXTERNAL_SOURCE_ERROR


class UnauthorizedActionError(SaratealError):
    status_code = 403
    error_code = ErrorCode.UNAUTHORIZED_ACTION


def required_field_error(field: str) -> ErrorDetail:
    return ErrorDetail(
        field=field,
        message="This field is required.",
    )


def positive_number_error(field: str, value: Any) -> ErrorDetail:
    return ErrorDetail(
        field=field,
        message="This value must be greater than zero.",
        value=value,
    )


def duplicate_record_error(
    entity: str,
    field: str,
    value: Any,
) -> DuplicateRecordError:
    return DuplicateRecordError(
        message=f"{entity} already exists.",
        details=[
            ErrorDetail(
                field=field,
                message=f"A {entity.lower()} with this {field} already exists.",
                value=value,
            )
        ],
        context={
            "entity": entity,
            "field": field,
        },
    )


def record_not_found_error(
    entity: str,
    identifier: Any,
) -> RecordNotFoundError:
    return RecordNotFoundError(
        message=f"{entity} was not found.",
        context={
            "entity": entity,
            "identifier": identifier,
        },
    )