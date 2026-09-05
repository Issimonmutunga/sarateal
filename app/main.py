from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    counties_router,
    county_weather_router,
    geocoding_router,
    health_router,
    market_weather_router,
    markets_router,
    products_router,
    weather_router,
)
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)


app.include_router(health_router)
app.include_router(counties_router)
app.include_router(products_router)
app.include_router(markets_router)
app.include_router(weather_router)
app.include_router(county_weather_router)
app.include_router(market_weather_router)
app.include_router(geocoding_router)