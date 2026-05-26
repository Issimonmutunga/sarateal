from app.data_sources.locations import find_county_coordinate
from app.services.weather_forecast import get_weather_risk_forecast
from app.services.weather_signals import WeatherRiskSignal


def get_county_weather_risk_forecast(
    county: str,
    forecast_days: int = 7,
) -> list[WeatherRiskSignal]:
    coordinate = find_county_coordinate(county=county)

    if coordinate is None:
        return []

    return get_weather_risk_forecast(
        latitude=coordinate.latitude,
        longitude=coordinate.longitude,
        forecast_days=forecast_days,
    )