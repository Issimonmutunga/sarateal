import pytest

from app.core.exceptions import DuplicateRecordError, RecordNotFoundError
from app.schemas.market import MarketCreate
from app.services.markets import create_market, get_market_or_raise, list_markets


def test_create_market_adds_market(db_session):
    market = create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Wakulima Market",
            county="Nairobi",
            market_type="wholesale",
            description="Major fresh produce market.",
        ),
    )

    assert market.id is not None
    assert market.name == "Wakulima Market"
    assert market.county == "Nairobi"
    assert market.market_type == "wholesale"
    assert market.is_active is True


def test_list_markets_returns_created_markets(db_session):
    create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Kongowea Market",
            county="Mombasa",
            market_type="wholesale",
        ),
    )

    markets = list_markets(db=db_session)

    assert len(markets) == 1
    assert markets[0].name == "Kongowea Market"


def test_create_market_rejects_duplicate_name_in_same_county(db_session):
    create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Main Market",
            county="Meru",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_market(
            db=db_session,
            market_in=MarketCreate(
                name="Main Market",
                county="Meru",
            ),
        )


def test_create_market_allows_same_name_in_different_counties(db_session):
    create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Main Market",
            county="Meru",
        ),
    )

    second_market = create_market(
        db=db_session,
        market_in=MarketCreate(
            name="Main Market",
            county="Nakuru",
        ),
    )

    assert second_market.id is not None
    assert second_market.county == "Nakuru"


def test_get_market_or_raise_rejects_unknown_market(db_session):
    with pytest.raises(RecordNotFoundError):
        get_market_or_raise(db=db_session, market_id=999999)