from datetime import date
from decimal import Decimal

from app.data_sources.prices.kenya_market_price_adapter import (
    KenyaMarketPriceRecord,
)
from app.services.kenya_market_price_ingestion import (
    fetch_raw_price_records_from_adapter,
)


class FakeKenyaMarketPriceAdapter:
    def fetch_prices(self) -> list[KenyaMarketPriceRecord]:
        return [
            KenyaMarketPriceRecord(
                product_name="Maize",
                county="Nairobi",
                unit="90kg bag",
                price=Decimal("4200.00"),
                currency="KES",
                observed_on=date(2026, 5, 29),
                source_name="Test market feed",
                source_url="https://example.com/prices.csv",
                market_name="Wakulima Market",
                notes="Wholesale price",
            ),
            KenyaMarketPriceRecord(
                product_name="Beans",
                county="Nakuru",
                unit="kg",
                price=Decimal("160.50"),
                currency="KES",
                observed_on=date(2026, 5, 29),
                source_name="Test market feed",
            ),
        ]


def test_fetch_raw_price_records_from_adapter_maps_price_fields():
    raw_records = fetch_raw_price_records_from_adapter(
        FakeKenyaMarketPriceAdapter(),
    )

    assert len(raw_records) == 2

    assert raw_records[0].product_name == "Maize"
    assert raw_records[0].county == "Nairobi"
    assert raw_records[0].unit == "90kg bag"
    assert raw_records[0].price == Decimal("4200.00")
    assert raw_records[0].observed_on == date(2026, 5, 29)
    assert raw_records[0].source_name == "Test market feed"
    assert raw_records[0].source_url == "https://example.com/prices.csv"


def test_fetch_raw_price_records_from_adapter_combines_market_and_notes():
    raw_records = fetch_raw_price_records_from_adapter(
        FakeKenyaMarketPriceAdapter(),
    )

    assert raw_records[0].notes == "Market: Wakulima Market | Wholesale price"


def test_fetch_raw_price_records_from_adapter_allows_missing_optional_notes():
    raw_records = fetch_raw_price_records_from_adapter(
        FakeKenyaMarketPriceAdapter(),
    )

    assert raw_records[1].product_name == "Beans"
    assert raw_records[1].source_url is None
    assert raw_records[1].notes is None