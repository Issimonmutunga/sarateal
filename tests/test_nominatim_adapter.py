import pytest

from app.data_sources.locations.nominatim import (
    NOMINATIM_SEARCH_URL,
    GeocodedLocation,
    build_nominatim_search_params,
    fetch_nominatim_location,
    parse_nominatim_search_result,
    parse_nominatim_search_results,
)


def test_build_nominatim_search_params_defaults_to_kenya():
    params = build_nominatim_search_params(
        query="Wakulima Market Nairobi",
    )

    assert params == {
        "q": "Wakulima Market Nairobi, Kenya",
        "format": "json",
        "limit": 1,
    }


def test_build_nominatim_search_params_allows_custom_country_and_limit():
    params = build_nominatim_search_params(
        query="Kampala Central Market",
        country="Uganda",
        limit=3,
    )

    assert params == {
        "q": "Kampala Central Market, Uganda",
        "format": "json",
        "limit": 3,
    }


def test_build_nominatim_search_params_strips_query_and_country_spaces():
    params = build_nominatim_search_params(
        query="  Kibuye Market Kisumu  ",
        country="  Kenya  ",
        limit=2,
    )

    assert params == {
        "q": "Kibuye Market Kisumu, Kenya",
        "format": "json",
        "limit": 2,
    }


def test_parse_nominatim_search_result_returns_geocoded_location():
    result = {
        "display_name": "Wakulima Market, Nairobi, Kenya",
        "lat": "-1.28333",
        "lon": "36.83333",
    }

    location = parse_nominatim_search_result(result)

    assert location == GeocodedLocation(
        display_name="Wakulima Market, Nairobi, Kenya",
        latitude=-1.28333,
        longitude=36.83333,
    )


def test_parse_nominatim_search_results_returns_all_locations():
    results = [
        {
            "display_name": "Wakulima Market, Nairobi, Kenya",
            "lat": "-1.28333",
            "lon": "36.83333",
        },
        {
            "display_name": "Kibuye Market, Kisumu, Kenya",
            "lat": "-0.09170",
            "lon": "34.76796",
        },
    ]

    locations = parse_nominatim_search_results(results)

    assert locations == [
        GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        ),
        GeocodedLocation(
            display_name="Kibuye Market, Kisumu, Kenya",
            latitude=-0.09170,
            longitude=34.76796,
        ),
    ]


def test_parse_nominatim_search_results_returns_empty_list_for_empty_results():
    locations = parse_nominatim_search_results([])

    assert locations == []


def test_parse_nominatim_search_result_requires_display_name():
    result = {
        "lat": "-1.28333",
        "lon": "36.83333",
    }

    with pytest.raises(KeyError):
        parse_nominatim_search_result(result)


def test_parse_nominatim_search_result_requires_latitude():
    result = {
        "display_name": "Wakulima Market, Nairobi, Kenya",
        "lon": "36.83333",
    }

    with pytest.raises(KeyError):
        parse_nominatim_search_result(result)


def test_parse_nominatim_search_result_requires_longitude():
    result = {
        "display_name": "Wakulima Market, Nairobi, Kenya",
        "lat": "-1.28333",
    }

    with pytest.raises(KeyError):
        parse_nominatim_search_result(result)


def test_fetch_nominatim_location_sends_expected_request_and_parses_response(
    monkeypatch,
):
    captured_request = {}

    class FakeResponse:
        def raise_for_status(self):
            captured_request["raise_for_status_called"] = True

        def json(self):
            return [
                {
                    "display_name": "Wakulima Market, Nairobi, Kenya",
                    "lat": "-1.28333",
                    "lon": "36.83333",
                }
            ]

    def fake_get(url, params, headers, timeout):
        captured_request["url"] = url
        captured_request["params"] = params
        captured_request["headers"] = headers
        captured_request["timeout"] = timeout

        return FakeResponse()

    monkeypatch.setattr(
        "app.data_sources.locations.nominatim.requests.get",
        fake_get,
    )

    locations = fetch_nominatim_location(
        query="Wakulima Market Nairobi",
        user_agent="sarateal-test/0.1",
        country="Kenya",
        limit=1,
        timeout_seconds=5,
    )

    assert captured_request == {
        "url": NOMINATIM_SEARCH_URL,
        "params": {
            "q": "Wakulima Market Nairobi, Kenya",
            "format": "json",
            "limit": 1,
        },
        "headers": {
            "User-Agent": "sarateal-test/0.1",
        },
        "timeout": 5,
        "raise_for_status_called": True,
    }

    assert locations == [
        GeocodedLocation(
            display_name="Wakulima Market, Nairobi, Kenya",
            latitude=-1.28333,
            longitude=36.83333,
        )
    ]