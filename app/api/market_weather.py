from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.market_weather import get_market_weather_risk_forecast


router = APIRouter(prefix="/market-weather", tags=["market-weather"])


class MarketWeatherRiskSignalRead(BaseModel):
    latitude: float
    longitude: float
    signal_date: date
    heat_risk: str
    rainfall_signal: str
    summary: str
    source_name: str


@router.get("/forecast", response_model=list[MarketWeatherRiskSignalRead])
def read_market_weather_risk_forecast(
    market_name: str,
    county: str | None = None,
    forecast_days: int = 7,
):
    return get_market_weather_risk_forecast(
        market_name=market_name,
        county=county,
        forecast_days=forecast_days,
    )