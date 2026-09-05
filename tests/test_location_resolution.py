from app.services.location_resolution import (
    resolve_county_coordinate,
    resolve_market_coordinate,
)


def test_resolve_market_coordinate_returns_none_for_blank_market_name():
    resolved_coordinate = resolve_market_coordinate(
        market_name="   ",
        county="Nairobi",
    )

    assert resolved_coordinate is None


def test_resolve_market_coordinate_uses_static_registry():
    resolved_coordinate = resolve_market_coordinate(
        market_name="Kibuye Market",
        county="Kisumu",
    )

    assert resolved_coordinate is not None
    assert resolved_coordinate.name == "Kibuye Market"
    assert resolved_coordinate.country == "Kenya"
    assert resolved_coordinate.location_type == "market"
    assert resolved_coordinate.source_name == "Static Kenya market coordinate registry"
    assert resolved_coordinate.is_verified is True


def test_resolve_market_coordinate_returns_none_when_location_unknown():
    resolved_coordinate = resolve_market_coordinate(
        market_name="Unknown Market",
        county="Unknown",
    )

    assert resolved_coordinate is None


def test_resolve_county_coordinate_returns_none_for_blank_county():
    resolved_coordinate = resolve_county_coordinate(
        county="   ",
    )

    assert resolved_coordinate is None


def test_resolve_county_coordinate_uses_static_registry():
    resolved_coordinate = resolve_county_coordinate(
        county="Kisumu",
    )

    assert resolved_coordinate is not None
    assert resolved_coordinate.name == "Kisumu"
    assert resolved_coordinate.country == "Kenya"
    assert resolved_coordinate.location_type == "county"
    assert resolved_coordinate.source_name == "Static Kenya county coordinate registry"
    assert resolved_coordinate.is_verified is True


def test_resolve_county_coordinate_returns_none_when_location_unknown():
    resolved_coordinate = resolve_county_coordinate(
        county="Unknown County",
    )

    assert resolved_coordinate is None