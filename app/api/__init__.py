from app.api.buyers import router as buyers_router
from app.api.buyer_demand import router as buyer_demand_router
from app.api.counties import router as counties_router
from app.api.farmers import router as farmers_router
from app.api.farmer_supply import router as farmer_supply_router
from app.api.health import router as health_router
from app.api.markets import router as markets_router
from app.api.match_generation import router as match_generation_router
from app.api.matches import router as matches_router
from app.api.prices import router as prices_router
from app.api.products import router as products_router
from app.api.tenders import router as tenders_router

__all__ = [
    "buyers_router",
    "buyer_demand_router",
    "counties_router",
    "farmers_router",
    "farmer_supply_router",
    "health_router",
    "markets_router",
    "match_generation_router",
    "matches_router",
    "prices_router",
    "products_router",
    "tenders_router",
]