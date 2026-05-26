from dataclasses import dataclass


@dataclass(frozen=True)
class CountyCoordinate:
    county: str
    latitude: float
    longitude: float
    location_type: str = "county"


KENYA_COUNTY_COORDINATES: list[CountyCoordinate] = [
    CountyCoordinate(county="Nairobi", latitude=-1.286389, longitude=36.817223),
    CountyCoordinate(county="Mombasa", latitude=-4.043477, longitude=39.668206),
    CountyCoordinate(county="Kisumu", latitude=-0.091702, longitude=34.767956),
    CountyCoordinate(county="Nakuru", latitude=-0.303099, longitude=36.080025),
    CountyCoordinate(county="Meru", latitude=0.046260, longitude=37.655872),
    CountyCoordinate(county="Uasin Gishu", latitude=0.514277, longitude=35.269779),
    CountyCoordinate(county="Bungoma", latitude=0.563500, longitude=34.560600),
    CountyCoordinate(county="Kakamega", latitude=0.282731, longitude=34.751863),
    CountyCoordinate(county="Kitui", latitude=-1.374800, longitude=38.010600),
    CountyCoordinate(county="Turkana", latitude=3.312247, longitude=35.565786),
    CountyCoordinate(county="Wajir", latitude=1.747100, longitude=40.057300),
    CountyCoordinate(county="Mandera", latitude=3.936600, longitude=41.867000),
    CountyCoordinate(county="Garissa", latitude=-0.453229, longitude=39.646099),
]


def list_county_coordinates() -> list[CountyCoordinate]:
    return KENYA_COUNTY_COORDINATES


def find_county_coordinate(county: str) -> CountyCoordinate | None:
    normalized_county = county.strip().lower()

    for coordinate in KENYA_COUNTY_COORDINATES:
        if coordinate.county.lower() == normalized_county:
            return coordinate

    return None