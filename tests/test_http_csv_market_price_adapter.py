from datetime import date
from decimal import Decimal

from app.data_sources.prices.http_csv_market_price_adapter import (
    HttpCsvKenyaMarketPriceAdapter,
)


def test_http_csv_adapter_parses_csv_text_into_price_records():
    adapter = HttpCsvKenyaMarketPriceAdapter(
        source_url="https://example.com/prices.csv",
        source_name="Test CSV feed",
    )

    csv_text = "\n".join(
        [
            "product_name,county,unit,price,currency,observed_on,market_name,notes",
            "Maize,Nairobi,90kg bag,4200.00,KES,2026-05-29,Wakulima Market,Wholesale",
            "Beans,Nakuru,kg,160.50,KES,2026-05-29,Nakuru Market,",
        ]
    )

    records = adapter._parse_csv_text(csv_text)

    assert len(records) == 2

    assert records[0].product_name == "Maize"
    assert records[0].county == "Nairobi"
    assert records[0].unit == "90kg bag"
    assert records[0].price == Decimal("4200.00")
    assert records[0].currency == "KES"
    assert records[0].observed_on == date(2026, 5, 29)
    assert records[0].source_name == "Test CSV feed"
    assert records[0].source_url == "https://example.com/prices.csv"
    assert records[0].market_name == "Wakulima Market"
    assert records[0].notes == "Wholesale"

    assert records[1].product_name == "Beans"
    assert records[1].notes is None


def test_http_csv_adapter_accepts_custom_column_map():
    adapter = HttpCsvKenyaMarketPriceAdapter(
        source_url="https://example.com/prices.csv",
        source_name="Custom CSV feed",
        column_map={
            "product_name": "commodity",
            "county": "region",
            "unit": "measure",
            "price": "value",
            "currency": "currency_code",
            "observed_on": "date_seen",
            "market_name": "market",
            "notes": "comment",
        },
    )

    csv_text = "\n".join(
        [
            "commodity,region,measure,value,currency_code,date_seen,market,comment",
            "Rice,Mombasa,kg,210.75,KES,2026-05-29,Kongowea Market,Retail",
        ]
    )

    records = adapter._parse_csv_text(csv_text)

    assert len(records) == 1
    assert records[0].product_name == "Rice"
    assert records[0].county == "Mombasa"
    assert records[0].unit == "kg"
    assert records[0].price == Decimal("210.75")
    assert records[0].currency == "KES"
    assert records[0].observed_on == date(2026, 5, 29)
    assert records[0].market_name == "Kongowea Market"
    assert records[0].notes == "Retail"


def test_http_csv_adapter_raises_error_for_missing_required_field():
    adapter = HttpCsvKenyaMarketPriceAdapter(
        source_url="https://example.com/prices.csv",
        source_name="Broken CSV feed",
    )

    csv_text = "\n".join(
        [
            "product_name,county,unit,price,currency,observed_on",
            "Maize,Nairobi,90kg bag,,KES,2026-05-29",
        ]
    )

    try:
        adapter._parse_csv_text(csv_text)
    except ValueError as error:
        assert str(error) == "Missing required price field: price"
    else:
        raise AssertionError("Expected missing price field to raise ValueError")