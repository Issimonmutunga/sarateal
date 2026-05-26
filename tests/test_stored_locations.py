from app.data_sources.locations.nominatim import GeocodedLocation
from app.services.stored_locations import (
    create_stored_location,
    get_stored_location,
    normalize_location_name,
)


def test_normalize_location_name_strips_lowercases_and_collapses_spaces():
    normalized_name = normalize_location_name("  Wakulima   Market   Nairobi  ")

    assert normalized_name == "wakulima market nairobi"


def test_normalize_location_name_returns_empty_string_for_blank_name():
    normalized_name = normalize_location_name("   ")

    assert normalized_name == ""


def test_create_stored_location_saves_location(db_session):
    geocoded_location = GeocodedLocation(
        display_name="Wakulima Market, Nairobi, Kenya",
        latitude=-1.28333,
        longitude=36.83333,
    )

    stored_location = create_stored_location(
        db=db_session,
        location_name="Wakulima Market Nairobi",
        geocoded_location=geocoded_location,
        country="Kenya",
    )

    assert stored_location.id is not None
    assert stored_location.location_name == "Wakulima Market Nairobi"
    assert stored_location.normalized_name == "wakulima market nairobi"
    assert stored_location.country == "Kenya"
    assert stored_location.latitude == -1.28333
    assert stored_location.longitude == 36.83333
    assert stored_location.source_name == "OpenStreetMap Nominatim"
    assert stored_location.source_display_name == "Wakulima Market, Nairobi, Kenya"
    assert stored_location.is_verified is False


def test_get_stored_location_returns_matching_location(db_session):
    geocoded_location = GeocodedLocation(
        display_name="Kibuye Market, Kisumu, Kenya",
        latitude=-0.09170,
        longitude=34.76796,
    )

    create_stored_location(
        db=db_session,
        location_name="Kibuye Market Kisumu",
        geocoded_location=geocoded_location,
        country="Kenya",
    )

    stored_location = get_stored_location(
        db=db_session,
        location_name="  KIBUYE   market kisumu ",
        country="Kenya",
    )

    assert stored_location is not None
    assert stored_location.location_name == "Kibuye Market Kisumu"
    assert stored_location.latitude == -0.09170
    assert stored_location.longitude == 34.76796


def test_get_stored_location_returns_none_for_unknown_location(db_session):
    stored_location = get_stored_location(
        db=db_session,
        location_name="Unknown Market",
        country="Kenya",
    )

    assert stored_location is None