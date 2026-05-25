from app.data_sources.locations import (
    LocationCoordinate,
    find_market_coordinate,
    list_market_coordinates,
)


def test_list_market_coordinates_returns_seed_coordinates():
    coordinates = list_market_coordinates()

    assert len(coordinates) > 0
    assert all(isinstance(coordinate, LocationCoordinate) for coordinate in coordinates)


def test_find_market_coordinate_returns_known_market():
    coordinate = find_market_coordinate(
        name="Wakulima Market",
        county="Nairobi",
    )

    assert coordinate is not None
    assert coordinate.name == "Wakulima Market"
    assert coordinate.county == "Nairobi"
    assert coordinate.latitude == -1.286389
    assert coordinate.longitude == 36.817223


def test_find_market_coordinate_is_case_insensitive():
    coordinate = find_market_coordinate(
        name="wakulima market",
        county="nairobi",
    )

    assert coordinate is not None
    assert coordinate.name == "Wakulima Market"


def test_find_market_coordinate_returns_none_for_unknown_market():
    coordinate = find_market_coordinate(
        name="Unknown Market",
        county="Nairobi",
    )

    assert coordinate is None