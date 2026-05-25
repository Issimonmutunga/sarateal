from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app.services.weather_signals import WeatherRiskSignal


client = TestClient(app)


def test_weather_forecast_endpoint_returns_weather_risk_signals(monkeypatch):
    def fake_get_weather_risk_forecast(
        latitude: float,
        longitude: float,
        forecast_days: int = 7,
    ):
        return [
            WeatherRiskSignal(
                latitude=latitude,
                longitude=longitude,
                signal_date=date(2026, 5, 25),
                heat_risk="high",
                rainfall_signal="dry",
                summary="High heat and dry conditions may stress crops and increase supply risk.",
                source_name="Open-Meteo",
            )
        ]

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

    payload = response.json()

    assert len(payload) == 1
    assert payload[0]["latitude"] == -1.286389
    assert payload[0]["longitude"] == 36.817223
    assert payload[0]["signal_date"] == "2026-05-25"
    assert payload[0]["heat_risk"] == "high"
    assert payload[0]["rainfall_signal"] == "dry"
    assert payload[0]["source_name"] == "Open-Meteo"