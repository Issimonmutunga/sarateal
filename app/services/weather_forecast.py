from app.data_sources.weather import fetch_open_meteo_daily_forecast
from app.services.weather_signals import WeatherRiskSignal, build_weather_risk_signals


def get_weather_risk_forecast(
    latitude: float,
    longitude: float,
    forecast_days: int = 7,
) -> list[WeatherRiskSignal]:
    weather_records = fetch_open_meteo_daily_forecast(
        latitude=latitude,
        longitude=longitude,
        forecast_days=forecast_days,
    )

    return build_weather_risk_signals(weather_records)