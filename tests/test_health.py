from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_route_returns_api_metadata():
    response = client.get("/")

    assert response.status_code == 200

    payload = response.json()

    assert payload["message"] == "Sarateal API is running"
    assert payload["docs"] == "/docs"
    assert payload["health"] == "/health"


def test_health_route_returns_application_status():
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["app"] == "Sarateal"
    assert payload["version"] == "0.1.0"
    assert payload["environment"] == "development"