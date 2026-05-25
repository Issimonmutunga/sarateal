from datetime import date

import pytest

from app.core.exceptions import RecordNotFoundError, BusinessRuleViolationError
from app.schemas.market import MarketCreate
from app.schemas.price import PriceCreate
from app.schemas.product import ProductCreate
from app.services.markets import create_market
from app.services.prices import create_price, get_price_or_raise, list_prices
from app.services.products import create_product


def create_test_product(db_session):
    return create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Maize",
            category="cereal",
            unit="kg",
        ),
    )


def create_test_market(db_session):
    return create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Wakulima Market",
            county="Nairobi",
            market_type="wholesale",
        ),
    )


def test_create_price_adds_price_record(db_session):
    product = create_test_product(db_session)
    market = create_test_market(db_session)

    price = create_price(
        db=db_session,
        price_in=PriceCreate(
            product_id=product.id,
            market_id=market.id,
            county="Nairobi",
            unit="kg",
            price=45.5,
            observed_on=date(2026, 5, 25),
            source_name="Test Source",
            source_url="https://example.com/prices",
            confidence_score=0.9,
        ),
    )

    assert price.id is not None
    assert price.product_id == product.id
    assert price.market_id == market.id
    assert price.county == "Nairobi"
    assert price.price == 45.5
    assert price.currency == "KES"


def test_list_prices_returns_created_prices(db_session):
    product = create_test_product(db_session)

    create_price(
        db=db_session,
        price_in=PriceCreate(
            product_id=product.id,
            county="Meru",
            unit="kg",
            price=40,
            observed_on=date(2026, 5, 25),
            source_name="Test Source",
        ),
    )

    prices = list_prices(db=db_session)

    assert len(prices) == 1
    assert prices[0].county == "Meru"


def test_get_price_or_raise_rejects_unknown_price(db_session):
    with pytest.raises(RecordNotFoundError):
        get_price_or_raise(db=db_session, price_id=999999)


def test_create_price_rejects_unknown_product(db_session):
    with pytest.raises(RecordNotFoundError):
        create_price(
            db=db_session,
            price_in=PriceCreate(
                product_id=999999,
                county="Meru",
                unit="kg",
                price=40,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
            ),
        )


def test_create_price_rejects_unknown_market(db_session):
    product = create_test_product(db_session)

    with pytest.raises(RecordNotFoundError):
        create_price(
            db=db_session,
            price_in=PriceCreate(
                product_id=product.id,
                market_id=999999,
                county="Meru",
                unit="kg",
                price=40,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
            ),
        )


def test_create_price_rejects_negative_price(db_session):
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_price(
            db=db_session,
            price_in=PriceCreate(
                product_id=product.id,
                county="Meru",
                unit="kg",
                price=-1,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
            ),
        )


def test_create_price_rejects_confidence_score_outside_zero_to_one(db_session):
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_price(
            db=db_session,
            price_in=PriceCreate(
                product_id=product.id,
                county="Meru",
                unit="kg",
                price=40,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
                confidence_score=1.5,
            ),
        )


def test_create_price_rejects_invalid_source_url(db_session):
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_price(
            db=db_session,
            price_in=PriceCreate(
                product_id=product.id,
                county="Meru",
                unit="kg",
                price=40,
                observed_on=date(2026, 5, 25),
                source_name="Test Source",
                source_url="ftp://example.com/prices",
            ),
        )