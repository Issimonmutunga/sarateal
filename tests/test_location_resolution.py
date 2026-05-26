from app.data_sources.locations.nominatim import GeocodedLocation
from app.services.location_resolution import (
    resolve_market_coordinate,
)
from app.services.stored_locations import create_stored_location


def test_resolve_market_coordinate_returns_none_for_blank_market_name(db_session):
    resolved_coordinate = resolve_market_coordinate(
        db=db_session,
        market_name="   ",
        county="Nairobi",
    )

    assert resolved_coordinate is None


def test_resolve_market_coordinate_prefers_verified_cache(db_session):
    create_stored_location(
        db=db_session,
        location_name="Wakulima Market",
        geocoded_location=GeocodedLocation(
            display_name="Verified Wakulima Market, Nairobi, Kenya",
            latitude=-1.28,
            longitude=36.82,
        ),
        country="Kenya",
        is_verified=True,
    )

    resolved_coordinate = resolve_market_coordinate(
        db=db_session,
        market_name="Wakulima Market",
        county="Nairobi",
    )

    assert resolved_coordinate is not None
    assert resolved_coordinate.name == "Wakulima Market"
    assert resolved_coordinate.latitude == -1.28
    assert resolved_coordinate.longitude == 36.82
    assert resolved_coordinate.location_type == "verified_cached_market"
    assert resolved_coordinate.source_name == "OpenStreetMap Nominatim"
    assert resolved_coordinate.is_verified is True


def test_resolve_market_coordinate_uses_static_registry_when_cache_is_unverified(
    db_session,
):
    create_stored_location(
        db=db_session,
        location_name="Wakulima Market",
        geocoded_location=GeocodedLocation(
            display_name="Unverified Wakulima Market, Nairobi, Kenya",
            latitude=-1.28,
            longitude=36.82,
        ),
        country="Kenya",
        is_verified=False,
    )

    resolved_coordinate = resolve_market_coordinate(
        db=db_session,
        market_name="Wakulima Market",
        county="Nairobi",
    )

    assert resolved_coordinate is not None
    assert resolved_coordinate.name == "Wakulima Market"
    assert resolved_coordinate.location_type == "market"
    assert resolved_coordinate.source_name == "Static Kenya market coordinate registry"
    assert resolved_coordinate.is_verified is True


def test_resolve_market_coordinate_uses_static_registry_when_no_cache(db_session):
    resolved_coordinate = resolve_market_coordinate(
        db=db_session,
        market_name="Kibuye Market",
        county="Kisumu",
    )

    assert resolved_coordinate is not None
    assert resolved_coordinate.name == "Kibuye Market"
    assert resolved_coordinate.country == "Kenya"
    assert resolved_coordinate.location_type == "market"
    assert resolved_coordinate.source_name == "Static Kenya market coordinate registry"
    assert resolved_coordinate.is_verified is True


def test_resolve_market_coordinate_uses_unverified_cache_when_static_missing(
    db_session,
):
    create_stored_location(
        db=db_session,
        location_name="New Local Market",
        geocoded_location=GeocodedLocation(
            display_name="New Local Market, Kenya",
            latitude=-0.5,
            longitude=37.1,
        ),
        country="Kenya",
        is_verified=False,
    )

    resolved_coordinate = resolve_market_coordinate(
        db=db_session,
        market_name="New Local Market",
        county="Unknown",
    )

    assert resolved_coordinate is not None
    assert resolved_coordinate.name == "New Local Market"
    assert resolved_coordinate.latitude == -0.5
    assert resolved_coordinate.longitude == 37.1
    assert resolved_coordinate.location_type == "cached_market"
    assert resolved_coordinate.is_verified is False


def test_resolve_market_coordinate_returns_none_when_location_unknown(db_session):
    resolved_coordinate = resolve_market_coordinate(
        db=db_session,
        market_name="Unknown Market",
        county="Unknown",
    )

    assert resolved_coordinate is None