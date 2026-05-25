from datetime import date

import pytest

from app.data_sources.prices.csv_adapter import (
    parse_optional_float,
    parse_price_date,
    read_price_csv,
    validate_csv_columns,
)


def test_parse_price_date_reads_iso_date():
    assert parse_price_date("2026-05-25") == date(2026, 5, 25)


def test_parse_optional_float_returns_default_for_blank_values():
    assert parse_optional_float(None, default=1.0) == 1.0
    assert parse_optional_float("   ", default=1.0) == 1.0


def test_parse_optional_float_reads_number():
    assert parse_optional_float("0.85", default=1.0) == 0.85


def test_validate_csv_columns_accepts_required_columns():
    validate_csv_columns(
        [
            "product_name",
            "county",
            "unit",
            "price",
            "observed_on",
            "source_name",
        ]
    )


def test_validate_csv_columns_rejects_missing_required_columns():
    with pytest.raises(ValueError):
        validate_csv_columns(["product_name", "county"])


def test_read_price_csv_returns_raw_price_records(tmp_path):
    csv_path = tmp_path / "prices.csv"
    csv_path.write_text(
        "\n".join(
            [
                "product_name,county,unit,price,observed_on,source_name,market_name,source_url,confidence_score,notes",
                "Maize,Nairobi,kg,45.5,2026-05-25,Manual Survey,Wakulima Market,https://example.com,0.9,Good quality",
                "Beans,Meru,kg,120,2026-05-25,Manual Survey,,,,",
            ]
        ),
        encoding="utf-8",
    )

    records = read_price_csv(csv_path)

    assert len(records) == 2
    assert records[0].product_name == "Maize"
    assert records[0].county == "Nairobi"
    assert records[0].unit == "kg"
    assert records[0].price == 45.5
    assert records[0].observed_on == date(2026, 5, 25)
    assert records[0].source_name == "Manual Survey"
    assert records[0].market_name == "Wakulima Market"
    assert records[0].source_url == "https://example.com"
    assert records[0].confidence_score == 0.9
    assert records[0].notes == "Good quality"

    assert records[1].product_name == "Beans"
    assert records[1].confidence_score == 1.0