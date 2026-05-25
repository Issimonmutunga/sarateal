from dataclasses import dataclass


@dataclass(frozen=True)
class LocationCoordinate:
    name: str
    county: str
    latitude: float
    longitude: float
    location_type: str = "market"


KENYA_MARKET_COORDINATES: list[LocationCoordinate] = [
    LocationCoordinate(
        name="Wakulima Market",
        county="Nairobi",
        latitude=-1.286389,
        longitude=36.817223,
    ),
    LocationCoordinate(
        name="Kongowea Market",
        county="Mombasa",
        latitude=-4.043477,
        longitude=39.668206,
    ),
    LocationCoordinate(
        name="Kibuye Market",
        county="Kisumu",
        latitude=-0.091702,
        longitude=34.767956,
    ),
    LocationCoordinate(
        name="Nakuru Market",
        county="Nakuru",
        latitude=-0.303099,
        longitude=36.080025,
    ),
    LocationCoordinate(
        name="Meru Market",
        county="Meru",
        latitude=0.046260,
        longitude=37.655872,
    ),
]


def list_market_coordinates() -> list[LocationCoordinate]:
    return KENYA_MARKET_COORDINATES


def find_market_coordinate(
    name: str,
    county: str | None = None,
) -> LocationCoordinate | None:
    normalized_name = name.strip().lower()
    normalized_county = county.strip().lower() if county else None

    for coordinate in KENYA_MARKET_COORDINATES:
        if coordinate.name.lower() != normalized_name:
            continue

        if normalized_county and coordinate.county.lower() != normalized_county:
            continue

        return coordinate

    return None