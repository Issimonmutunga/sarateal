from app.schemas.product import ProductCreate
from app.services.price_csv_ingestion import ingest_price_csv
from app.services.products import create_product


def test_ingest_price_csv_creates_prices_for_known_products(db_session, tmp_path):
    create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Maize",
            category="cereal",
            unit="kg",
        ),
    )

    csv_path = tmp_path / "prices.csv"
    csv_path.write_text(
        "\n".join(
            [
                "product_name,county,unit,price,observed_on,source_name,market_name,source_url,confidence_score,notes",
                "Maize,Nairobi,kg,45.5,2026-05-25,Manual Survey,,https://example.com,0.9,Good quality",
                "Unknown Crop,Nairobi,kg,30,2026-05-25,Manual Survey,,,,",
            ]
        ),
        encoding="utf-8",
    )

    prices = ingest_price_csv(
        db=db_session,
        file_path=csv_path,
    )

    assert len(prices) == 1
    assert prices[0].county == "Nairobi"
    assert prices[0].price == 45.5
    assert prices[0].source_name == "Manual Survey"