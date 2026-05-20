from datetime import date
from typing import Any

from app.core.exceptions import (
    BusinessRuleViolationError,
    ErrorDetail,
)


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = " ".join(value.strip().split())

    if not cleaned:
        return None

    return cleaned


def normalize_required_text(value: str, field: str) -> str:
    cleaned = normalize_text(value)

    if not cleaned:
        raise BusinessRuleViolationError(
            message="Required text validation failed.",
            details=[
                ErrorDetail(
                    field=field,
                    message="This field is required and cannot be empty.",
                    value=value,
                )
            ],
            context={
                "field": field,
            },
        )

    return cleaned


def validate_positive_number(
    value: float,
    field: str,
    *,
    entity: str,
) -> None:
    if value <= 0:
        raise BusinessRuleViolationError(
            message=f"{entity} validation failed.",
            details=[
                ErrorDetail(
                    field=field,
                    message="This value must be greater than zero.",
                    value=value,
                )
            ],
            context={
                "entity": entity,
                "field": field,
            },
        )


def validate_non_negative_number(
    value: float | None,
    field: str,
    *,
    entity: str,
) -> None:
    if value is not None and value < 0:
        raise BusinessRuleViolationError(
            message=f"{entity} validation failed.",
            details=[
                ErrorDetail(
                    field=field,
                    message="This value cannot be negative.",
                    value=value,
                )
            ],
            context={
                "entity": entity,
                "field": field,
            },
        )


def validate_date_order(
    start_date: date | None,
    end_date: date | None,
    *,
    start_field: str,
    end_field: str,
    entity: str,
) -> None:
    if start_date and end_date and end_date < start_date:
        raise BusinessRuleViolationError(
            message=f"{entity} date validation failed.",
            details=[
                ErrorDetail(
                    field=end_field,
                    message=f"{end_field} cannot be earlier than {start_field}.",
                    value=end_date,
                )
            ],
            context={
                "entity": entity,
                "start_field": start_field,
                "end_field": end_field,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )


def validate_url(
    value: str | None,
    field: str,
    *,
    entity: str,
    required: bool = False,
) -> None:
    cleaned = normalize_text(value)

    if required and not cleaned:
        raise BusinessRuleViolationError(
            message=f"{entity} URL validation failed.",
            details=[
                ErrorDetail(
                    field=field,
                    message="This URL is required.",
                    value=value,
                )
            ],
            context={
                "entity": entity,
                "field": field,
            },
        )

    if cleaned and not cleaned.startswith(("http://", "https://")):
        raise BusinessRuleViolationError(
            message=f"{entity} URL validation failed.",
            details=[
                ErrorDetail(
                    field=field,
                    message="URL must start with http:// or https://.",
                    value=value,
                )
            ],
            context={
                "entity": entity,
                "field": field,
            },
        )


def validate_score_range(
    value: float,
    field: str,
    *,
    entity: str,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> None:
    if value < minimum or value > maximum:
        raise BusinessRuleViolationError(
            message=f"{entity} score validation failed.",
            details=[
                ErrorDetail(
                    field=field,
                    message=f"This value must be between {minimum} and {maximum}.",
                    value=value,
                )
            ],
            context={
                "entity": entity,
                "field": field,
                "minimum": minimum,
                "maximum": maximum,
            },
        )


def collect_date_order_error(
    details: list[ErrorDetail],
    start_date: date | None,
    end_date: date | None,
    *,
    start_field: str,
    end_field: str,
) -> None:
    if start_date and end_date and end_date < start_date:
        details.append(
            ErrorDetail(
                field=end_field,
                message=f"{end_field} cannot be earlier than {start_field}.",
                value=end_date,
            )
        )


def collect_positive_number_error(
    details: list[ErrorDetail],
    value: float,
    field: str,
) -> None:
    if value <= 0:
        details.append(
            ErrorDetail(
                field=field,
                message="This value must be greater than zero.",
                value=value,
            )
        )


def collect_non_negative_number_error(
    details: list[ErrorDetail],
    value: float | None,
    field: str,
) -> None:
    if value is not None and value < 0:
        details.append(
            ErrorDetail(
                field=field,
                message="This value cannot be negative.",
                value=value,
            )
        )


def raise_if_details(
    details: list[ErrorDetail],
    *,
    message: str,
    entity: str,
    context: dict[str, Any] | None = None,
) -> None:
    if not details:
        return

    raise BusinessRuleViolationError(
        message=message,
        details=details,
        context={
            "entity": entity,
            **(context or {}),
        },
    )