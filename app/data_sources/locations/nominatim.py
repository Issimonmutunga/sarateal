from __future__ import annotations

from dataclasses import dataclass

import requests


NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"


@dataclass(frozen=True)
class GeocodedLocation:
    display_name: str
    latitude: float
    longitude: float
    source_name: str = "OpenStreetMap Nominatim"


def build_nominatim_search_params(
    query: str,
    country: str = "Kenya",
    limit: int = 1,
) -> dict[str, str | int]:
    clean_query = query.strip()

    if country:
        clean_query = f"{clean_query}, {country.strip()}"

    return {
        "q": clean_query,
        "format": "json",
        "limit": limit,
    }


def parse_nominatim_search_result(result: dict) -> GeocodedLocation:
    return GeocodedLocation(
        display_name=str(result["display_name"]),
        latitude=float(result["lat"]),
        longitude=float(result["lon"]),
    )


def parse_nominatim_search_results(results: list[dict]) -> list[GeocodedLocation]:
    return [parse_nominatim_search_result(result) for result in results]


def fetch_nominatim_location(
    query: str,
    user_agent: str,
    country: str = "Kenya",
    limit: int = 1,
    timeout_seconds: int = 10,
) -> list[GeocodedLocation]:
    params = build_nominatim_search_params(
        query=query,
        country=country,
        limit=limit,
    )

    response = requests.get(
        NOMINATIM_SEARCH_URL,
        params=params,
        headers={
            "User-Agent": user_agent,
        },
        timeout=timeout_seconds,
    )

    response.raise_for_status()

    return parse_nominatim_search_results(response.json())