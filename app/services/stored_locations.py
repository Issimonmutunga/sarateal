"""In-memory store for geocoded location cache entries.

The read-only/stateless backend keeps a tiny process-local cache so
repeated geocoding lookups don't hit Nominatim. It is not persisted;
entries are lost on restart, which is acceptable for this footprint.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count


@dataclass
class StoredLocation:
    id: int
    location_name: str
    normalized_name: str
    country: str
    latitude: float
    longitude: float
    source_name: str
    source_display_name: str | None = None
    is_verified: bool = False


def normalize_location_name(location_name: str) -> str:
    return " ".join(location_name.strip().lower().split())


_next_id = count(1)
_records: dict[int, StoredLocation] = {}
_index: dict[tuple[str, str], int] = {}


def clear_stored_locations() -> None:
    _records.clear()
    _index.clear()


def get_stored_location(
    location_name: str,
    country: str = "Kenya",
) -> StoredLocation | None:
    normalized_name = normalize_location_name(location_name)

    if not normalized_name:
        return None

    record_id = _index.get((normalized_name, country.strip()))

    if record_id is None:
        return None

    return _records.get(record_id)


def get_stored_location_by_id(
    stored_location_id: int,
) -> StoredLocation | None:
    return _records.get(stored_location_id)


def create_stored_location(
    location_name: str,
    geocoded_location,
    country: str = "Kenya",
    is_verified: bool = False,
) -> StoredLocation:
    stored_location = StoredLocation(
        id=next(_next_id),
        location_name=location_name.strip(),
        normalized_name=normalize_location_name(location_name),
        country=country.strip(),
        latitude=geocoded_location.latitude,
        longitude=geocoded_location.longitude,
        source_name=geocoded_location.source_name,
        source_display_name=geocoded_location.display_name,
        is_verified=is_verified,
    )

    _index[(stored_location.normalized_name, stored_location.country)] = (
        stored_location.id
    )
    _records[stored_location.id] = stored_location

    return stored_location


def list_stored_locations(
    country: str | None = None,
    verified_only: bool | None = None,
) -> list[StoredLocation]:
    locations = sorted(
        _records.values(),
        key=lambda location: location.location_name,
    )

    if country is not None:
        locations = [
            location
            for location in locations
            if location.country == country.strip()
        ]

    if verified_only is not None:
        locations = [
            location
            for location in locations
            if location.is_verified == verified_only
        ]

    return locations


def set_stored_location_verification(
    stored_location_id: int,
    is_verified: bool,
) -> StoredLocation | None:
    stored_location = get_stored_location_by_id(stored_location_id)

    if stored_location is None:
        return None

    stored_location.is_verified = is_verified

    return stored_location