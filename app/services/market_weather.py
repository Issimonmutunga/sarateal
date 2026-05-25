from app.data_sources.locations import find_market_coordinate
from app.services.weather_forecast import get_weather_risk_forecast
from app.services.weather_signals import WeatherRiskSignal


def get_market_weather_risk_forecast(
    market_name: str,
    county: str | None = None,
    forecast_days: int = 7,
) -> list[WeatherRiskSignal]:
    coordinate = find_market_coordinate(
        name=market_name,
        county=county,
    )

    if coordinate is None:
        return []

    return get_weather_risk_forecast(
        latitude=coordinate.latitude,
        longitude=coordinate.longitude,
        forecast_days=forecast_days,
    )