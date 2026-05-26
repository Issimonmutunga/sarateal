from app.data_sources.locations.nominatim import GeocodedLocation
from app.services.geocoding import (
    DEFAULT_NOMINATIM_USER_AGENT,
    geocode_location_name,
    geocode_location_name_with_cache,
)
from app.services.stored_locations import create_stored_location, get_stored_location


def test_geocode_location_name_returns_empty_list_for_blank_name():
    locations = geocode_location_name("   ")

    assert locations == []


def test_geocode_location_name_calls_nominatim_with_clean_location_name(
    monkeypatch,
):
    captured_call = {}

    expected_locations = [
        GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        )
    ]

    def fake_fetch_nominatim_location(
        query: str,
        user_agent: str,
        country: str = "Kenya",
        limit: int = 1,
    ):
        captured_call["query"] = query
        captured_call["user_agent"] = user_agent
        captured_call["country"] = country
        captured_call["limit"] = limit

        return expected_locations

    monkeypatch.setattr(
        "app.services.geocoding.fetch_nominatim_location",
        fake_fetch_nominatim_location,
    )

    locations = geocode_location_name("  Wakulima Market Nairobi  ")

    assert captured_call == {
        "query": "Wakulima Market Nairobi",
        "user_agent": DEFAULT_NOMINATIM_USER_AGENT,
        "country": "Kenya",
        "limit": 1,
    }

    assert locations == expected_locations


def test_geocode_location_name_allows_custom_country_limit_and_user_agent(
    monkeypatch,
):
    captured_call = {}

    expected_locations = [
        GeocodedLocation(
            display_name="Kampala Central Market, Uganda",
            latitude=0.31361,
            longitude=32.58111,
        )
    ]

    def fake_fetch_nominatim_location(
        query: str,
        user_agent: str,
        country: str = "Kenya",
        limit: int = 1,
    ):
        captured_call["query"] = query
        captured_call["user_agent"] = user_agent
        captured_call["country"] = country
        captured_call["limit"] = limit

        return expected_locations

    monkeypatch.setattr(
        "app.services.geocoding.fetch_nominatim_location",
        fake_fetch_nominatim_location,
    )

    locations = geocode_location_name(
        location_name="Kampala Central Market",
        country="Uganda",
        limit=3,
        user_agent="sarateal-test/0.1",
    )

    assert captured_call == {
        "query": "Kampala Central Market",
        "user_agent": "sarateal-test/0.1",
        "country": "Uganda",
        "limit": 3,
    }

    assert locations == expected_locations


def test_geocode_location_name_with_cache_returns_empty_list_for_blank_name(
    db_session,
):
    locations = geocode_location_name_with_cache(
        db=db_session,
        location_name="   ",
    )

    assert locations == []


def test_geocode_location_name_with_cache_returns_cached_location_without_fetching(
    db_session,
    monkeypatch,
):
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

    def fake_fetch_nominatim_location(
        query: str,
        user_agent: str,
        country: str = "Kenya",
        limit: int = 1,
    ):
        raise AssertionError("Nominatim should not be called on cache hit.")

    monkeypatch.setattr(
        "app.services.geocoding.fetch_nominatim_location",
        fake_fetch_nominatim_location,
    )

    locations = geocode_location_name_with_cache(
        db=db_session,
        location_name="  WAKULIMA   market nairobi ",
        country="Kenya",
    )

    assert locations == [
        GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        )
    ]


def test_geocode_location_name_with_cache_fetches_and_saves_on_cache_miss(
    db_session,
    monkeypatch,
):
    captured_call = {}

    expected_locations = [
        GeocodedLocation(
            display_name="Kibuye Market, Kisumu, Kenya",
            latitude=-0.09170,
            longitude=34.76796,
        )
    ]

    def fake_fetch_nominatim_location(
        query: str,
        user_agent: str,
        country: str = "Kenya",
        limit: int = 1,
    ):
        captured_call["query"] = query
        captured_call["user_agent"] = user_agent
        captured_call["country"] = country
        captured_call["limit"] = limit

        return expected_locations

    monkeypatch.setattr(
        "app.services.geocoding.fetch_nominatim_location",
        fake_fetch_nominatim_location,
    )

    locations = geocode_location_name_with_cache(
        db=db_session,
        location_name="  Kibuye Market Kisumu  ",
        country="Kenya",
        limit=1,
        user_agent="sarateal-test/0.1",
    )

    stored_location = get_stored_location(
        db=db_session,
        location_name="kibuye market kisumu",
        country="Kenya",
    )

    assert captured_call == {
        "query": "Kibuye Market Kisumu",
        "user_agent": "sarateal-test/0.1",
        "country": "Kenya",
        "limit": 1,
    }

    assert locations == expected_locations
    assert stored_location is not None
    assert stored_location.latitude == -0.09170
    assert stored_location.longitude == 34.76796


def test_geocode_location_name_with_cache_does_not_save_when_fetch_returns_empty(
    db_session,
    monkeypatch,
):
    def fake_fetch_nominatim_location(
        query: str,
        user_agent: str,
        country: str = "Kenya",
        limit: int = 1,
    ):
        return []

    monkeypatch.setattr(
        "app.services.geocoding.fetch_nominatim_location",
        fake_fetch_nominatim_location,
    )

    locations = geocode_location_name_with_cache(
        db=db_session,
        location_name="Unknown Market",
        country="Kenya",
    )

    stored_location = get_stored_location(
        db=db_session,
        location_name="Unknown Market",
        country="Kenya",
    )

    assert locations == []
    assert stored_location is None