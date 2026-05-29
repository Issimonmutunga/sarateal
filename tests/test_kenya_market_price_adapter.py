from datetime import date
from decimal import Decimal

from app.data_sources.prices.kenya_market_price_adapter import (
    KenyaMarketPriceRecord,
)


def test_kenya_market_price_record_stores_required_price_fields():
    record = KenyaMarketPriceRecord(
        product_name="Maize",
        county="Nairobi",
        unit="90kg bag",
        price=Decimal("4200.00"),
        currency="KES",
        observed_on=date(2026, 5, 29),
        source_name="Test source",
    )

    assert record.product_name == "Maize"
    assert record.county == "Nairobi"
    assert record.unit == "90kg bag"
    assert record.price == Decimal("4200.00")
    assert record.currency == "KES"
    assert record.observed_on == date(2026, 5, 29)
    assert record.source_name == "Test source"
    assert record.source_url is None
    assert record.market_name is None
    assert record.notes is None


def test_kenya_market_price_record_accepts_optional_source_details():
    record = KenyaMarketPriceRecord(
        product_name="Beans",
        county="Nakuru",
        unit="kg",
        price=Decimal("160.50"),
        currency="KES",
        observed_on=date(2026, 5, 29),
        source_name="County market bulletin",
        source_url="https://example.com/prices",
        market_name="Nakuru Market",
        notes="Wholesale estimate",
    )

    assert record.source_url == "https://example.com/prices"
    assert record.market_name == "Nakuru Market"
    assert record.notes == "Wholesale estimate"