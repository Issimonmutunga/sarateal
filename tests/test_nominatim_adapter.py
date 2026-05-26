import pytest

from app.data_sources.locations.nominatim import (
    GeocodedLocation,
    build_nominatim_search_params,
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