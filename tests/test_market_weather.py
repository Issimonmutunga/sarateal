from datetime import date

from app.services.market_weather import get_market_weather_risk_forecast
from app.services.weather_signals import WeatherRiskSignal


def test_get_market_weather_risk_forecast_returns_signals_for_known_market(
    db_session,
    monkeypatch,
):
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
                heat_risk="medium",
                rainfall_signal="light_rain",
                summary="Rainfall is present and should be monitored for market and logistics effects.",
                source_name="Open-Meteo",
            )
        ]

    monkeypatch.setattr(
        "app.services.market_weather.get_weather_risk_forecast",
        fake_get_weather_risk_forecast,
    )

    signals = get_market_weather_risk_forecast(
        db=db_session,
        market_name="Wakulima Market",
        county="Nairobi",
        forecast_days=1,
    )

    assert len(signals) == 1
    assert signals[0].latitude == -1.286389
    assert signals[0].longitude == 36.817223
    assert signals[0].heat_risk == "medium"


def test_get_market_weather_risk_forecast_returns_empty_list_for_unknown_market(
    db_session,
):
    signals = get_market_weather_risk_forecast(
        db=db_session,
        market_name="Unknown Market",
        county="Nairobi",
        forecast_days=1,
    )

    assert signals == []