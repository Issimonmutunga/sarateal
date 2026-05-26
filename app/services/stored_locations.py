from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_sources.locations.nominatim import GeocodedLocation
from app.models.stored_location import StoredLocation


def normalize_location_name(location_name: str) -> str:
    return " ".join(location_name.strip().lower().split())


def get_stored_location(
    db: Session,
    location_name: str,
    country: str = "Kenya",
) -> StoredLocation | None:
    normalized_name = normalize_location_name(location_name)

    if not normalized_name:
        return None

    statement = select(StoredLocation).where(
        StoredLocation.normalized_name == normalized_name,
        StoredLocation.country == country.strip(),
    )

    return db.scalar(statement)


def create_stored_location(
    db: Session,
    location_name: str,
    geocoded_location: GeocodedLocation,
    country: str = "Kenya",
    is_verified: bool = False,
) -> StoredLocation:
    stored_location = StoredLocation(
        location_name=location_name.strip(),
        normalized_name=normalize_location_name(location_name),
        country=country.strip(),
        latitude=geocoded_location.latitude,
        longitude=geocoded_location.longitude,
        source_name=geocoded_location.source_name,
        source_display_name=geocoded_location.display_name,
        is_verified=is_verified,
    )

    db.add(stored_location)
    db.commit()
    db.refresh(stored_location)

    return stored_location