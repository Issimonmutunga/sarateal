from __future__ import annotations

from dataclasses import dataclass

from app.data_sources.locations import (
    find_county_coordinate,
    find_market_coordinate,
)
from app.data_sources.locations.kenya_county_coordinates import CountyCoordinate
from app.data_sources.locations.kenya_market_coordinates import LocationCoordinate


@dataclass(frozen=True)
class ResolvedLocationCoordinate:
    name: str
    country: str
    latitude: float
    longitude: float
    location_type: str
    source_name: str
    is_verified: bool = False


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


def county_coordinate_to_resolved_coordinate(
    county_coordinate: CountyCoordinate,
    country: str = "Kenya",
) -> ResolvedLocationCoordinate:
    return ResolvedLocationCoordinate(
        name=county_coordinate.county,
        country=country,
        latitude=county_coordinate.latitude,
        longitude=county_coordinate.longitude,
        location_type=county_coordinate.location_type,
        source_name="Static Kenya county coordinate registry",
        is_verified=True,
    )


def resolve_market_coordinate(
    market_name: str,
    county: str | None = None,
    country: str = "Kenya",
) -> ResolvedLocationCoordinate | None:
    clean_market_name = market_name.strip()

    if not clean_market_name:
        return None

    market_coordinate = find_market_coordinate(
        clean_market_name,
        county,
    )

    if market_coordinate is not None:
        return market_coordinate_to_resolved_coordinate(
            market_coordinate=market_coordinate,
            country=country,
        )

    return None


def resolve_county_coordinate(
    county: str,
    country: str = "Kenya",
) -> ResolvedLocationCoordinate | None:
    clean_county = county.strip()

    if not clean_county:
        return None

    county_coordinate = find_county_coordinate(clean_county)

    if county_coordinate is not None:
        return county_coordinate_to_resolved_coordinate(
            county_coordinate=county_coordinate,
            country=country,
        )

    return None