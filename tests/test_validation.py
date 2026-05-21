from datetime import date

import pytest

from app.core.exceptions import BusinessRuleViolationError
from app.core.validators import (
    collect_date_order_error,
    collect_non_negative_number_error,
    collect_positive_number_error,
    normalize_required_text,
    normalize_text,
    raise_if_details,
    validate_date_order,
    validate_non_negative_number,
    validate_positive_number,
    validate_score_range,
    validate_url,
)


def test_normalize_text_strips_and_collapses_whitespace():
    assert normalize_text("  Maize  ") == "Maize"
    assert normalize_text("  Maize   Grade   A  ") == "Maize Grade A"
    assert normalize_text("") is None
    assert normalize_text("   ") is None
    assert normalize_text(None) is None


def test_normalize_required_text_accepts_cleanable_values():
    assert normalize_required_text("  Maize  ", field="name") == "Maize"


def test_normalize_required_text_rejects_blank_values():
    with pytest.raises(BusinessRuleViolationError):
        normalize_required_text("   ", field="name")


def test_validate_positive_number_accepts_positive_values():
    assert validate_positive_number(
        10,
        field="quantity",
        entity="FarmerSupply",
    ) is None


def test_validate_positive_number_rejects_zero_and_negative_values():
    with pytest.raises(BusinessRuleViolationError):
        validate_positive_number(
            0,
            field="quantity",
            entity="FarmerSupply",
        )

    with pytest.raises(BusinessRuleViolationError):
        validate_positive_number(
            -1,
            field="quantity",
            entity="FarmerSupply",
        )


def test_validate_non_negative_number_accepts_none_zero_and_positive_values():
    assert validate_non_negative_number(
        None,
        field="price",
        entity="FarmerSupply",
    ) is None
    assert validate_non_negative_number(
        0,
        field="price",
        entity="FarmerSupply",
    ) is None
    assert validate_non_negative_number(
        10,
        field="price",
        entity="FarmerSupply",
    ) is None


def test_validate_non_negative_number_rejects_negative_values():
    with pytest.raises(BusinessRuleViolationError):
        validate_non_negative_number(
            -1,
            field="price",
            entity="FarmerSupply",
        )


def test_validate_date_order_accepts_valid_date_range():
    assert validate_date_order(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 31),
        start_field="available_from",
        end_field="available_until",
        entity="FarmerSupply",
    ) is None


def test_validate_date_order_accepts_open_ended_dates():
    assert validate_date_order(
        start_date=date(2026, 1, 1),
        end_date=None,
        start_field="available_from",
        end_field="available_until",
        entity="FarmerSupply",
    ) is None


def test_validate_date_order_rejects_end_date_before_start_date():
    with pytest.raises(BusinessRuleViolationError):
        validate_date_order(
            start_date=date(2026, 1, 31),
            end_date=date(2026, 1, 1),
            start_field="available_from",
            end_field="available_until",
            entity="FarmerSupply",
        )


def test_validate_url_accepts_http_https_and_optional_blank_urls():
    assert validate_url(
        "https://example.com",
        field="source_url",
        entity="Tender",
    ) is None
    assert validate_url(
        "http://example.com",
        field="source_url",
        entity="Tender",
    ) is None
    assert validate_url(
        None,
        field="source_url",
        entity="Tender",
    ) is None


def test_validate_url_rejects_invalid_url_scheme():
    with pytest.raises(BusinessRuleViolationError):
        validate_url(
            "ftp://example.com",
            field="source_url",
            entity="Tender",
        )


def test_validate_score_range_accepts_scores_between_zero_and_one_hundred():
    assert validate_score_range(
        0,
        field="opportunity_score",
        entity="Match",
    ) is None
    assert validate_score_range(
        100,
        field="opportunity_score",
        entity="Match",
    ) is None


def test_validate_score_range_rejects_scores_outside_allowed_range():
    with pytest.raises(BusinessRuleViolationError):
        validate_score_range(
            -1,
            field="opportunity_score",
            entity="Match",
        )

    with pytest.raises(BusinessRuleViolationError):
        validate_score_range(
            101,
            field="opportunity_score",
            entity="Match",
        )


def test_collect_helpers_return_error_details_without_raising_immediately():
    details = []

    collect_positive_number_error(details, value=0, field="quantity")
    collect_non_negative_number_error(details, value=-1, field="price")
    collect_date_order_error(
        details,
        start_date=date(2026, 2, 1),
        end_date=date(2026, 1, 1),
        start_field="start_date",
        end_field="end_date",
    )

    assert len(details) == 3


def test_raise_if_details_raises_business_rule_error_when_details_exist():
    details = []

    collect_positive_number_error(details, value=0, field="quantity")

    with pytest.raises(BusinessRuleViolationError):
        raise_if_details(
            details,
            message="Validation failed.",
            entity="FarmerSupply",
        )