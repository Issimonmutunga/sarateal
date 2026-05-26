from app.models.stored_location import StoredLocation


def test_stored_location_model_can_be_created():
    location = StoredLocation(
        location_name="Wakulima Market Nairobi",
        normalized_name="wakulima market nairobi",
        country="Kenya",
        latitude=-1.28333,
        longitude=36.83333,
        source_name="OpenStreetMap Nominatim",
        source_display_name="Wakulima Market, Nairobi, Kenya",
        is_verified=False,
    )

    assert location.location_name == "Wakulima Market Nairobi"
    assert location.normalized_name == "wakulima market nairobi"
    assert location.country == "Kenya"
    assert location.latitude == -1.28333
    assert location.longitude == 36.83333
    assert location.source_name == "OpenStreetMap Nominatim"
    assert location.source_display_name == "Wakulima Market, Nairobi, Kenya"
    assert location.is_verified is False


def test_stored_location_model_can_mark_location_as_verified():
    location = StoredLocation(
        location_name="Kibuye Market Kisumu",
        normalized_name="kibuye market kisumu",
        country="Kenya",
        latitude=-0.09170,
        longitude=34.76796,
        is_verified=False,
    )

    location.is_verified = True

    assert location.is_verified is True