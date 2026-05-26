from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.county_weather import get_county_weather_risk_forecast


router = APIRouter(prefix="/county-weather", tags=["county-weather"])


class CountyWeatherRiskSignalRead(BaseModel):
    latitude: float
    longitude: float
    signal_date: date
    heat_risk: str
    rainfall_signal: str
    summary: str
    source_name: str


@router.get("/forecast", response_model=list[CountyWeatherRiskSignalRead])
def read_county_weather_risk_forecast(
    county: str,
    forecast_days: int = 7,
):
    return get_county_weather_risk_forecast(
        county=county,
        forecast_days=forecast_days,
    )