from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.weather_forecast import get_weather_risk_forecast


router = APIRouter(prefix="/weather", tags=["weather"])


class WeatherRiskSignalRead(BaseModel):
    latitude: float
    longitude: float
    signal_date: date
    heat_risk: str
    rainfall_signal: str
    summary: str
    source_name: str


@router.get("/forecast", response_model=list[WeatherRiskSignalRead])
def read_weather_risk_forecast(
    latitude: float,
    longitude: float,
    forecast_days: int = 7,
):
    return get_weather_risk_forecast(
        latitude=latitude,
        longitude=longitude,
        forecast_days=forecast_days,
    )