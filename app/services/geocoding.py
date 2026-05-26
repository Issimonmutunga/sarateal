from __future__ import annotations

from sqlalchemy.orm import Session

from app.data_sources.locations.nominatim import (
    GeocodedLocation,
    fetch_nominatim_location,
)
from app.services.stored_locations import (
    create_stored_location,
    get_stored_location,
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


def geocode_location_name_with_cache(
    db: Session,
    location_name: str,
    country: str = "Kenya",
    limit: int = 1,
    user_agent: str = DEFAULT_NOMINATIM_USER_AGENT,
) -> list[GeocodedLocation]:
    clean_location_name = location_name.strip()

    if not clean_location_name:
        return []

    stored_location = get_stored_location(
        db=db,
        location_name=clean_location_name,
        country=country,
    )

    if stored_location is not None:
        return [
            GeocodedLocation(
                display_name=stored_location.source_display_name
                or stored_location.location_name,
                latitude=stored_location.latitude,
                longitude=stored_location.longitude,
                source_name=stored_location.source_name,
            )
        ]

    geocoded_locations = fetch_nominatim_location(
        query=clean_location_name,
        user_agent=user_agent,
        country=country,
        limit=limit,
    )

    if geocoded_locations:
        create_stored_location(
            db=db,
            location_name=clean_location_name,
            geocoded_location=geocoded_locations[0],
            country=country,
        )

    return geocoded_locations