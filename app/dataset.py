"""Static, in-memory reference datasets.

The backend is stateless and runs well under Render's free-plan memory
limit (512 MB). Instead of a relational database, reference data is
loaded into memory at startup.

Only real reference data lives here (counties, products, markets with
published coordinates). No demo, simulated, or imputed records ever enter
the system: per the STMOI methodology, observations (supply, demand,
price) are recorded by real users and live signals (e.g. weather) are
fetched on demand from upstream providers.
"""

from __future__ import annotations

from pydantic import BaseModel

from app.data_sources import KENYA_COUNTIES, MVP_PRODUCTS
from app.data_sources.locations import (
    KENYA_COUNTY_COORDINATES,
    KENYA_MARKET_COORDINATES,
)


class CountyReadModel(BaseModel):
    id: int
    name: str
    code: str
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ProductReadModel(BaseModel):
    id: int
    name: str
    category: str
    unit: str
    is_active: bool = True


class MarketReadModel(BaseModel):
    id: int
    name: str
    county: str
    sub_county: str | None = None
    ward: str | None = None
    market_type: str = "general"
    description: str | None = None
    is_active: bool = True
    latitude: float | None = None
    longitude: float | None = None


_COUNTY_COORDS_BY_NAME = {
    coordinate.county: coordinate for coordinate in KENYA_COUNTY_COORDINATES
}

_MARKET_COORDS_BY_NAME = {
    coordinate.name: coordinate for coordinate in KENYA_MARKET_COORDINATES
}


def _county_coord_lat(county: str) -> float | None:
    coordinate = _COUNTY_COORDS_BY_NAME.get(county)
    return coordinate.latitude if coordinate else None


def _county_coord_lon(county: str) -> float | None:
    coordinate = _COUNTY_COORDS_BY_NAME.get(county)
    return coordinate.longitude if coordinate else None


COUNTIES = [
    CountyReadModel(
        id=index + 1,
        **raw,
        latitude=_county_coord_lat(raw["name"]),
        longitude=_county_coord_lon(raw["name"]),
    )
    for index, raw in enumerate(KENYA_COUNTIES)
]

COUNTY_ID_BY_CODE = {county.code: county.id for county in COUNTIES}
COUNTY_ID_BY_NAME = {county.name: county.id for county in COUNTIES}

PRODUCTS = [
    ProductReadModel(id=index + 1, **raw)
    for index, raw in enumerate(MVP_PRODUCTS)
]

PRODUCT_ID_BY_NAME = {product.name: product.id for product in PRODUCTS}


def _build_markets() -> list[MarketReadModel]:
    markets: list[MarketReadModel] = []
    market_type_by_name = {
        "Wakulima Market": "general",
        "Kongowea Market": "coastal",
        "Kibuye Market": "general",
        "Nakuru Market": "general",
        "Meru Market": "general",
    }

    for index, coordinate in enumerate(KENYA_MARKET_COORDINATES):
        markets.append(
            MarketReadModel(
                id=index + 1,
                name=coordinate.name,
                county=coordinate.county,
                market_type=market_type_by_name.get(coordinate.name, "general"),
                description=f"{coordinate.name} in {coordinate.county.title()}, Kenya.",
                latitude=coordinate.latitude,
                longitude=coordinate.longitude,
            )
        )

    return markets


MARKETS = _build_markets()
MARKET_ID_BY_NAME = {market.name: market.id for market in MARKETS}


def list_counties() -> list[CountyReadModel]:
    return COUNTIES


def get_county(county_id: int) -> CountyReadModel | None:
    for county in COUNTIES:
        if county.id == county_id:
            return county

    return None


def list_products(active_only: bool = True) -> list[ProductReadModel]:
    if not active_only:
        return PRODUCTS

    return [product for product in PRODUCTS if product.is_active]


def get_product(product_id: int) -> ProductReadModel | None:
    for product in PRODUCTS:
        if product.id == product_id:
            return product

    return None


def list_markets() -> list[MarketReadModel]:
    return MARKETS


def get_market(market_id: int) -> MarketReadModel | None:
    for market in MARKETS:
        if market.id == market_id:
            return market

    return None


def find_market_by_name(name: str) -> MarketReadModel | None:
    for market in MARKETS:
        if market.name == name:
            return market

    return None