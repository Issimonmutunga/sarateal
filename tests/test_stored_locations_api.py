from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_stored_locations_endpoint_returns_success(monkeypatch):
    def fake_list_stored_locations(
        db,
        country: str | None = None,
        verified_only: bool | None = None,
    ):
        return []

    monkeypatch.setattr(
        "app.api.stored_locations.list_stored_locations",
        fake_list_stored_locations,
    )

    response = client.get("/stored-locations")

    assert response.status_code == 200
    assert response.json() == []


def test_stored_locations_endpoint_passes_filters(monkeypatch):
    captured_call = {}

    def fake_list_stored_locations(
        db,
        country: str | None = None,
        verified_only: bool | None = None,
    ):
        captured_call["country"] = country
        captured_call["verified_only"] = verified_only

        return []

    monkeypatch.setattr(
        "app.api.stored_locations.list_stored_locations",
        fake_list_stored_locations,
    )

    response = client.get(
        "/stored-locations",
        params={
            "country": "Kenya",
            "verified_only": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == []
    assert captured_call == {
        "country": "Kenya",
        "verified_only": True,
    }


def test_stored_location_verification_endpoint_returns_success(monkeypatch):
    captured_call = {}

    def fake_set_stored_location_verification(
        db,
        stored_location_id: int,
        is_verified: bool,
    ):
        captured_call["stored_location_id"] = stored_location_id
        captured_call["is_verified"] = is_verified

        return {
            "id": stored_location_id,
            "location_name": "Wakulima Market Nairobi",
            "normalized_name": "wakulima market nairobi",
            "country": "Kenya",
            "latitude": -1.28333,
            "longitude": 36.83333,
            "source_name": "OpenStreetMap Nominatim",
            "source_display_name": "Wakulima Market, Nairobi, Kenya",
            "is_verified": is_verified,
        }

    monkeypatch.setattr(
        "app.api.stored_locations.set_stored_location_verification",
        fake_set_stored_location_verification,
    )

    response = client.patch(
        "/stored-locations/1/verification",
        params={
            "is_verified": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["is_verified"] is True
    assert captured_call == {
        "stored_location_id": 1,
        "is_verified": True,
    }


def test_stored_location_verification_endpoint_returns_404_for_unknown_location(
    monkeypatch,
):
    def fake_set_stored_location_verification(
        db,
        stored_location_id: int,
        is_verified: bool,
    ):
        return None

    monkeypatch.setattr(
        "app.api.stored_locations.set_stored_location_verification",
        fake_set_stored_location_verification,
    )

    response = client.patch(
        "/stored-locations/999999/verification",
        params={
            "is_verified": True,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Stored location not found.",
    }


def test_stored_location_verification_endpoint_requires_is_verified():
    response = client.patch("/stored-locations/1/verification")

    assert response.status_code == 422