from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app.services.weather_signals import WeatherRiskSignal


client = TestClient(app)


def test_market_weather_forecast_endpoint_returns_signals(monkeypatch):
    def fake_get_market_weather_risk_forecast(
        db,
        market_name: str,
        county: str | None = None,
        forecast_days: int = 7,
    ):
        return [
            WeatherRiskSignal(
                latitude=-1.286389,
                longitude=36.817223,
                signal_date=date(2026, 5, 25),
                heat_risk="medium",
                rainfall_signal="light_rain",
                summary="Rainfall is present and should be monitored for market and logistics effects.",
                source_name="Open-Meteo",
            )
        ]

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

    payload = response.json()

    assert len(payload) == 1
    assert payload[0]["latitude"] == -1.286389
    assert payload[0]["longitude"] == 36.817223
    assert payload[0]["signal_date"] == "2026-05-25"
    assert payload[0]["heat_risk"] == "medium"
    assert payload[0]["rainfall_signal"] == "light_rain"
    assert payload[0]["source_name"] == "Open-Meteo"