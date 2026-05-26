from app.api.buyers import router as buyers_router
from app.api.buyer_demand import router as buyer_demand_router
from app.api.counties import router as counties_router
from app.api.county_weather import router as county_weather_router
from app.api.farmers import router as farmers_router
from app.api.farmer_supply import router as farmer_supply_router
from app.api.health import router as health_router
from app.api.market_weather import router as market_weather_router
from app.api.markets import router as markets_router
from app.api.match_generation import router as match_generation_router
from app.api.matches import router as matches_router
from app.api.price_ingestion import router as price_ingestion_router
from app.api.prices import router as prices_router
from app.api.products import router as products_router
from app.api.tenders import router as tenders_router
from app.api.weather import router as weather_router

__all__ = [
    "buyers_router",
    "buyer_demand_router",
    "counties_router",
    "county_weather_router",
    "farmer_supply_router",
    "farmers_router",
    "health_router",
    "market_weather_router",
    "markets_router",
    "match_generation_router",
    "matches_router",
    "price_ingestion_router",
    "prices_router",
    "products_router",
    "tenders_router",
    "weather_router",
]