from app.data_sources.kenya_counties import KENYA_COUNTIES
from app.data_sources.locations import (
    CountyCoordinate,
    find_county_coordinate,
    list_county_coordinates,
)


def test_county_coordinates_cover_all_kenyan_counties():
    county_names = {county["name"] for county in KENYA_COUNTIES}
    coordinate_names = {
        coordinate.county for coordinate in list_county_coordinates()
    }

    assert len(coordinate_names) == len(KENYA_COUNTIES) == 47
    assert coordinate_names == county_names


def test_list_county_coordinates_returns_seed_coordinates():
    coordinates = list_county_coordinates()

    assert len(coordinates) > 0
    assert all(isinstance(coordinate, CountyCoordinate) for coordinate in coordinates)


def test_find_county_coordinate_returns_known_county():
    coordinate = find_county_coordinate("Nairobi")

    assert coordinate is not None
    assert coordinate.county == "Nairobi"
    assert coordinate.latitude == -1.286389
    assert coordinate.longitude == 36.817223


def test_find_county_coordinate_is_case_insensitive():
    coordinate = find_county_coordinate("nairobi")

    assert coordinate is not None
    assert coordinate.county == "Nairobi"


def test_find_county_coordinate_returns_none_for_unknown_county():
    coordinate = find_county_coordinate("Unknown County")

    assert coordinate is None