from datetime import date

from app.data_sources.weather import DailyWeatherRecord
from app.services.weather_forecast import get_weather_risk_forecast


def test_get_weather_risk_forecast_builds_signals_from_open_meteo_records(monkeypatch):
    def fake_fetch_open_meteo_daily_forecast(
        latitude: float,
        longitude: float,
        forecast_days: int,
    ):
        return [
            DailyWeatherRecord(
                latitude=latitude,
                longitude=longitude,
                forecast_date=date(2026, 5, 25),
                max_temperature_c=36,
                min_temperature_c=18,
                precipitation_mm=0,
            )
        ]

    monkeypatch.setattr(
        "app.services.weather_forecast.fetch_open_meteo_daily_forecast",
        fake_fetch_open_meteo_daily_forecast,
    )

    signals = get_weather_risk_forecast(
        latitude=-1.286389,
        longitude=36.817223,
        forecast_days=1,
    )

    assert len(signals) == 1
    assert signals[0].heat_risk == "high"
    assert signals[0].rainfall_signal == "dry"
    assert signals[0].source_name == "Open-Meteo"