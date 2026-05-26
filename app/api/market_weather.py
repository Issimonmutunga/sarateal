from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
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
    market_name: str = Query(..., min_length=1),
    county: str | None = Query(default=None, min_length=1),
    forecast_days: int = Query(default=7, ge=1, le=16),
    db: Session = Depends(get_db),
):
    return get_market_weather_risk_forecast(
        db=db,
        market_name=market_name,
        county=county,
        forecast_days=forecast_days,
    )