from app.data_sources.locations.nominatim import GeocodedLocation
from app.services.stored_locations import (
    create_stored_location,
    get_stored_location,
    get_stored_location_by_id,
    list_stored_locations,
    normalize_location_name,
    set_stored_location_verification,
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


def test_get_stored_location_by_id_returns_matching_location(db_session):
    created_location = create_stored_location(
        db=db_session,
        location_name="Wakulima Market Nairobi",
        geocoded_location=GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        ),
        country="Kenya",
    )

    stored_location = get_stored_location_by_id(
        db=db_session,
        stored_location_id=created_location.id,
    )

    assert stored_location is not None
    assert stored_location.id == created_location.id
    assert stored_location.location_name == "Wakulima Market Nairobi"


def test_get_stored_location_by_id_returns_none_for_unknown_id(db_session):
    stored_location = get_stored_location_by_id(
        db=db_session,
        stored_location_id=999999,
    )

    assert stored_location is None


def test_set_stored_location_verification_updates_verified_status(db_session):
    stored_location = create_stored_location(
        db=db_session,
        location_name="Verified Market",
        geocoded_location=GeocodedLocation(
            display_name="Verified Market, Kenya",
            latitude=-1.1,
            longitude=36.1,
        ),
        country="Kenya",
        is_verified=False,
    )

    updated_location = set_stored_location_verification(
        db=db_session,
        stored_location_id=stored_location.id,
        is_verified=True,
    )

    assert updated_location is not None
    assert updated_location.id == stored_location.id
    assert updated_location.is_verified is True


def test_set_stored_location_verification_returns_none_for_unknown_id(db_session):
    updated_location = set_stored_location_verification(
        db=db_session,
        stored_location_id=999999,
        is_verified=True,
    )

    assert updated_location is None


def test_list_stored_locations_returns_all_locations_ordered_by_name(db_session):
    create_stored_location(
        db=db_session,
        location_name="Wakulima Market Nairobi",
        geocoded_location=GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        ),
        country="Kenya",
    )
    create_stored_location(
        db=db_session,
        location_name="Kibuye Market Kisumu",
        geocoded_location=GeocodedLocation(
            display_name="Kibuye Market, Kisumu, Kenya",
            latitude=-0.09170,
            longitude=34.76796,
        ),
        country="Kenya",
    )

    locations = list_stored_locations(db=db_session)

    assert [location.location_name for location in locations] == [
        "Kibuye Market Kisumu",
        "Wakulima Market Nairobi",
    ]


def test_list_stored_locations_can_filter_by_country(db_session):
    create_stored_location(
        db=db_session,
        location_name="Wakulima Market Nairobi",
        geocoded_location=GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        ),
        country="Kenya",
    )
    create_stored_location(
        db=db_session,
        location_name="Kampala Central Market",
        geocoded_location=GeocodedLocation(
            display_name="Kampala Central Market, Uganda",
            latitude=0.31361,
            longitude=32.58111,
        ),
        country="Uganda",
    )

    locations = list_stored_locations(
        db=db_session,
        country="Uganda",
    )

    assert len(locations) == 1
    assert locations[0].location_name == "Kampala Central Market"


def test_list_stored_locations_can_filter_by_verified_status(db_session):
    create_stored_location(
        db=db_session,
        location_name="Unverified Market",
        geocoded_location=GeocodedLocation(
            display_name="Unverified Market, Kenya",
            latitude=-1.0,
            longitude=36.0,
        ),
        country="Kenya",
        is_verified=False,
    )
    create_stored_location(
        db=db_session,
        location_name="Verified Market",
        geocoded_location=GeocodedLocation(
            display_name="Verified Market, Kenya",
            latitude=-1.1,
            longitude=36.1,
        ),
        country="Kenya",
        is_verified=True,
    )

    locations = list_stored_locations(
        db=db_session,
        verified_only=True,
    )

    assert len(locations) == 1
    assert locations[0].location_name == "Verified Market"
    assert locations[0].is_verified is True