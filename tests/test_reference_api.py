from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_counties_endpoint_returns_kenya_counties():
    response = client.get("/counties/")

    assert response.status_code == 200

    counties = response.json()

    assert len(counties) > 40
    assert any(county["name"] == "Nairobi" for county in counties)


def test_products_endpoint_returns_mvp_products():
    response = client.get("/products/")

    assert response.status_code == 200

    products = response.json()

    assert len(products) > 20
    assert any(product["name"] == "Maize" for product in products)
    assert all(product["is_active"] is True for product in products)


def test_markets_endpoint_returns_static_markets():
    response = client.get("/markets")

    assert response.status_code == 200

    markets = response.json()

    assert len(markets) > 0
    assert any(market["name"] == "Wakulima Market" for market in markets)