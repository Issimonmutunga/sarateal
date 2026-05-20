from fastapi import FastAPI

from app.api import (
    buyers_router,
    buyer_demand_router,
    counties_router,
    farmers_router,
    farmer_supply_router,
    match_generation_router,
    matches_router,
    products_router,
    tenders_router,
)
from app.core.config import get_settings
from app.db.init_db import init_db


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


app.include_router(counties_router)
app.include_router(products_router)
app.include_router(farmers_router)
app.include_router(buyers_router)
app.include_router(farmer_supply_router)
app.include_router(buyer_demand_router)
app.include_router(tenders_router)
app.include_router(matches_router)
app.include_router(match_generation_router)