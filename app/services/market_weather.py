from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.location_resolution import resolve_market_coordinate
from app.services.weather_forecast import get_weather_risk_forecast
from app.services.weather_signals import WeatherRiskSignal


def get_market_weather_risk_forecast(
    db: Session,
    market_name: str,
    county: str | None = None,
    forecast_days: int = 7,
) -> list[WeatherRiskSignal]:
    resolved_coordinate = resolve_market_coordinate(
        db=db,
        market_name=market_name,
        county=county,
    )

    if resolved_coordinate is None:
        return []

    return get_weather_risk_forecast(
        latitude=resolved_coordinate.latitude,
        longitude=resolved_coordinate.longitude,
        forecast_days=forecast_days,
    )