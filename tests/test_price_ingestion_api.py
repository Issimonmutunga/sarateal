from app.db.init_db import init_db
from app.main import app
from fastapi.testclient import TestClient


init_db()

client = TestClient(app)


def test_price_csv_ingestion_endpoint_accepts_file_path():
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