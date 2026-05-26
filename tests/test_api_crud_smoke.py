from fastapi.testclient import TestClient

from app.db.init_db import init_db
from app.main import app


init_db()

client = TestClient(app)


def test_core_list_routes_return_success():
    routes = [
        "/counties",
        "/products",
        "/markets",
        "/prices",
        "/farmers",
        "/buyers",
        "/farmer-supply",
        "/buyer-demand",
        "/tenders",
        "/matches",
    ]

    for route in routes:
        response = client.get(route)

        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_route_order_farmer_supply_farmer_path_is_not_treated_as_supply_id():
    response = client.get("/farmer-supply/farmer/999999")

    assert response.status_code in {200, 404}


def test_route_order_buyer_demand_buyer_path_is_not_treated_as_demand_id():
    response = client.get("/buyer-demand/buyer/999999")

    assert response.status_code in {200, 404}


def test_route_order_tenders_county_path_is_not_treated_as_tender_id():
    response = client.get("/tenders/county/Meru")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_route_order_matches_supply_path_is_not_treated_as_match_id():
    response = client.get("/matches/supply/999999")

    assert response.status_code in {200, 404}


def test_generate_supply_demand_matches_endpoint_returns_success():
    response = client.post("/match-generation/supply-demand")

    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload, list)


def test_price_csv_ingestion_endpoint_returns_success():
    response = client.post(
        "/price-ingestion/csv",
        json={
            "file_path": "data/raw/prices/sample_prices.csv",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert "prices_created" in payload
    assert isinstance(payload["prices_created"], int)


def test_weather_forecast_endpoint_is_registered(monkeypatch):
    def fake_get_weather_risk_forecast(
        latitude: float,
        longitude: float,
        forecast_days: int = 7,
    ):
        return []

    monkeypatch.setattr(
        "app.api.weather.get_weather_risk_forecast",
        fake_get_weather_risk_forecast,
    )

    response = client.get(
        "/weather/forecast",
        params={
            "latitude": -1.286389,
            "longitude": 36.817223,
            "forecast_days": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_market_weather_forecast_endpoint_is_registered(monkeypatch):
    def fake_get_market_weather_risk_forecast(
        market_name: str,
        county: str | None = None,
        forecast_days: int = 7,
    ):
        return []

    monkeypatch.setattr(
        "app.api.market_weather.get_market_weather_risk_forecast",
        fake_get_market_weather_risk_forecast,
    )

    response = client.get(
        "/market-weather/forecast",
        params={
            "market_name": "Wakulima Market",
            "county": "Nairobi",
            "forecast_days": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == []

def test_county_weather_forecast_endpoint_is_registered(monkeypatch):
    def fake_get_county_weather_risk_forecast(
        county: str,
        forecast_days: int = 7,
    ):
        return []

    monkeypatch.setattr(
        "app.api.county_weather.get_county_weather_risk_forecast",
        fake_get_county_weather_risk_forecast,
    )

    response = client.get(
        "/county-weather/forecast",
        params={
            "county": "Nairobi",
            "forecast_days": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == []

def test_geocoding_search_endpoint_is_registered(monkeypatch):
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

def test_docs_route_is_available():
    response = client.get("/docs")

    assert response.status_code == 200