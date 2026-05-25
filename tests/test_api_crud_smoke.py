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


def test_docs_route_is_available():
    response = client.get("/docs")

    assert response.status_code == 200