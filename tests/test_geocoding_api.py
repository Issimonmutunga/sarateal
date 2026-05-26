from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_geocoding_search_endpoint_returns_success(monkeypatch):
    def fake_geocode_location_name(
        location_name: str,
        country: str = "Kenya",
        limit: int = 1,
    ):
        return []

    monkeypatch.setattr(
        "app.api.geocoding.geocode_location_name",
        fake_geocode_location_name,
    )

    response = client.get(
        "/geocoding/search",
        params={
            "location_name": "Wakulima Market Nairobi",
            "country": "Kenya",
            "limit": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_geocoding_search_endpoint_requires_location_name():
    response = client.get(
        "/geocoding/search",
        params={
            "country": "Kenya",
            "limit": 1,
        },
    )

    assert response.status_code == 422


def test_geocoding_search_endpoint_rejects_zero_limit():
    response = client.get(
        "/geocoding/search",
        params={
            "location_name": "Wakulima Market Nairobi",
            "country": "Kenya",
            "limit": 0,
        },
    )

    assert response.status_code == 422