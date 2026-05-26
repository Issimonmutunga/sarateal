from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.data_sources.locations.kenya_market_coordinates import (
    LocationCoordinate,
    find_market_coordinate,
)
from app.models.stored_location import StoredLocation
from app.services.stored_locations import get_stored_location


@dataclass(frozen=True)
class ResolvedLocationCoordinate:
    name: str
    country: str
    latitude: float
    longitude: float
    location_type: str
    source_name: str
    is_verified: bool = False


def stored_location_to_resolved_coordinate(
    stored_location: StoredLocation,
    location_type: str = "stored_location",
) -> ResolvedLocationCoordinate:
    return ResolvedLocationCoordinate(
        name=stored_location.location_name,
        country=stored_location.country,
        latitude=stored_location.latitude,
        longitude=stored_location.longitude,
        location_type=location_type,
        source_name=stored_location.source_name,
        is_verified=stored_location.is_verified,
    )


def market_coordinate_to_resolved_coordinate(
    market_coordinate: LocationCoordinate,
    country: str = "Kenya",
) -> ResolvedLocationCoordinate:
    return ResolvedLocationCoordinate(
        name=market_coordinate.name,
        country=country,
        latitude=market_coordinate.latitude,
        longitude=market_coordinate.longitude,
        location_type=market_coordinate.location_type,
        source_name="Static Kenya market coordinate registry",
        is_verified=True,
    )


def resolve_market_coordinate(
    db: Session,
    market_name: str,
    county: str | None = None,
    country: str = "Kenya",
    prefer_verified_cache: bool = True,
) -> ResolvedLocationCoordinate | None:
    clean_market_name = market_name.strip()

    if not clean_market_name:
        return None

    stored_location = get_stored_location(
        db=db,
        location_name=clean_market_name,
        country=country,
    )

    if (
        prefer_verified_cache
        and stored_location is not None
        and stored_location.is_verified
    ):
        return stored_location_to_resolved_coordinate(
            stored_location=stored_location,
            location_type="verified_cached_market",
        )

    market_coordinate = find_market_coordinate(
        clean_market_name,
        county,
    )

    if market_coordinate is not None:
        return market_coordinate_to_resolved_coordinate(
            market_coordinate=market_coordinate,
            country=country,
        )

    if stored_location is not None:
        return stored_location_to_resolved_coordinate(
            stored_location=stored_location,
            location_type="cached_market",
        )

    return None