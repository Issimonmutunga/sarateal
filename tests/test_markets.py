from app.services.markets import get_market_service, list_markets_service


def test_list_markets_returns_registry_markets():
    markets = list_markets_service()

    assert len(markets) > 0
    assert any(market.name == "Wakulima Market" for market in markets)


def test_list_markets_include_county_and_type():
    markets = list_markets_service()
    wakulima = next(
        market for market in markets if market.name == "Wakulima Market"
    )

    assert wakulima.county == "Nairobi"
    assert wakulima.is_active is True


def test_get_market_returns_known_market():
    markets = list_markets_service()
    first_market = markets[0]

    market = get_market_service(first_market.id)

    assert market is not None
    assert market.id == first_market.id


def test_get_market_returns_none_for_unknown_id():
    market = get_market_service(999999)

    assert market is None