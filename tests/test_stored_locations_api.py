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