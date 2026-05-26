from app.data_sources.locations.nominatim import GeocodedLocation
from app.services.geocoding import (
    DEFAULT_NOMINATIM_USER_AGENT,
    geocode_location_name,
)


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