from fastapi import APIRouter, Query

from app.services.market_weather import get_market_weather_risk_forecast


router = APIRouter(prefix="/market-weather", tags=["market-weather"])


@router.get("/forecast")
def read_market_weather_risk_forecast(
    market_name: str = Query(..., min_length=1),
    county: str | None = Query(default=None, min_length=1),
    forecast_days: int = Query(default=7, ge=1, le=16),
):
    return get_market_weather_risk_forecast(
        market_name=market_name,
        county=county,
        forecast_days=forecast_days,
    )