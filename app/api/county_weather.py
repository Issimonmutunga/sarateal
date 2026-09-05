from fastapi import APIRouter, Query

from app.services.county_weather import get_county_weather_risk_forecast


router = APIRouter(prefix="/county-weather", tags=["county-weather"])


@router.get("/forecast")
def read_county_weather_risk_forecast(
    county: str = Query(..., min_length=1),
    forecast_days: int = Query(default=7, ge=1, le=16),
):
    return get_county_weather_risk_forecast(
        county=county,
        forecast_days=forecast_days,
    )