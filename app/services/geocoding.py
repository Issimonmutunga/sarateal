from __future__ import annotations

from app.data_sources.locations.nominatim import (
    GeocodedLocation,
    fetch_nominatim_location,
)


DEFAULT_NOMINATIM_USER_AGENT = "sarateal/0.1"


def geocode_location_name(
    location_name: str,
    country: str = "Kenya",
    limit: int = 1,
    user_agent: str = DEFAULT_NOMINATIM_USER_AGENT,
) -> list[GeocodedLocation]:
    clean_location_name = location_name.strip()

    if not clean_location_name:
        return []

    return fetch_nominatim_location(
        query=clean_location_name,
        user_agent=user_agent,
        country=country,
        limit=limit,
    )