from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.location_resolution import resolve_county_coordinate
from app.services.weather_forecast import get_weather_risk_forecast
from app.services.weather_signals import WeatherRiskSignal


def get_county_weather_risk_forecast(
    db: Session,
    county: str,
    forecast_days: int = 7,
) -> list[WeatherRiskSignal]:
    resolved_coordinate = resolve_county_coordinate(
        db=db,
        county=county,
    )

    if resolved_coordinate is None:
        return []

    return get_weather_risk_forecast(
        latitude=resolved_coordinate.latitude,
        longitude=resolved_coordinate.longitude,
        forecast_days=forecast_days,
    )