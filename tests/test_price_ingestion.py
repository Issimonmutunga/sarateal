from datetime import date

from app.data_sources.prices import RawPriceRecord
from app.schemas.market import MarketCreate
from app.schemas.product import ProductCreate
from app.services.markets import create_market
from app.services.price_ingestion import ingest_raw_price_record, ingest_raw_price_records
from app.services.products import create_product


def test_ingest_raw_price_record_creates_price_for_known_product(db_session):
    product = create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Maize",
            category="cereal",
            unit="kg",
        ),
    )

    price = ingest_raw_price_record(
        db=db_session,
        record=RawPriceRecord(
            product_name="Maize",
            county="Nairobi",
            unit="kg",
            price=45.5,
            observed_on=date(2026, 5, 25),
            source_name="Test Source",
        ),
    )

    assert price is not None
    assert price.product_id == product.id
    assert price.county == "Nairobi"
    assert price.price == 45.5


def test_ingest_raw_price_record_links_known_market(db_session):
    product = create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Beans",
            category="legume",
            unit="kg",
        ),
    )
    market = create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Wakulima Market",
            county="Nairobi",
            market_type="wholesale",
        ),
    )

    price = ingest_raw_price_record(
        db=db_session,
        record=RawPriceRecord(
            product_name="Beans",
            market_name="Wakulima Market",
            county="Nairobi",
            unit="kg",
            price=120,
            observed_on=date(2026, 5, 25),
            source_name="Test Source",
        ),
    )

    assert price is not None
    assert price.product_id == product.id
    assert price.market_id == market.id


def test_ingest_raw_price_record_skips_unknown_product(db_session):
    price = ingest_raw_price_record(
        db=db_session,
        record=RawPriceRecord(
            product_name="Unknown Crop",
            county="Nairobi",
            unit="kg",
            price=45.5,
            observed_on=date(2026, 5, 25),
            source_name="Test Source",
        ),
    )

    assert price is None


def test_ingest_raw_price_records_returns_only_created_prices(db_session):
    create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Tomatoes",
            category="vegetable",
            unit="kg",
        ),
    )

    prices = ingest_raw_price_records(
        db=db_session,
        records=[
            RawPriceRecord(
                product_name="Tomatoes",
                county="Nairobi",
                unit="kg",
                price=60,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
            ),
            RawPriceRecord(
                product_name="Unknown Crop",
                county="Nairobi",
                unit="kg",
                price=20,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
            ),
        ],
    )

    assert len(prices) == 1
    assert prices[0].price == 60