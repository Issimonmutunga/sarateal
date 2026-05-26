from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import (
    buyers_router,
    buyer_demand_router,
    counties_router,
    county_weather_router,
    farmer_supply_router,
    farmers_router,
    geocoding_router,
    health_router,
    market_weather_router,
    markets_router,
    match_generation_router,
    matches_router,
    price_ingestion_router,
    prices_router,
    products_router,
    stored_locations_router,
    tenders_router,
    weather_router,
)
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.db.init_db import init_db


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

register_exception_handlers(app)


app.include_router(health_router)
app.include_router(counties_router)
app.include_router(products_router)
app.include_router(markets_router)
app.include_router(prices_router)
app.include_router(price_ingestion_router)
app.include_router(weather_router)
app.include_router(market_weather_router)
app.include_router(county_weather_router)
app.include_router(geocoding_router)
app.include_router(stored_locations_router)
app.include_router(farmers_router)
app.include_router(buyers_router)
app.include_router(farmer_supply_router)
app.include_router(buyer_demand_router)
app.include_router(tenders_router)
app.include_router(matches_router)
app.include_router(match_generation_router)