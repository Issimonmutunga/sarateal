from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
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
    county: str = Query(..., min_length=1),
    forecast_days: int = Query(default=7, ge=1, le=16),
    db: Session = Depends(get_db),
):
    return get_county_weather_risk_forecast(
        db=db,
        county=county,
        forecast_days=forecast_days,
    )