from fastapi import APIRouter

from app.services.markets import get_market_service, list_markets_service


router = APIRouter(prefix="/markets", tags=["markets"])


@router.get("")
def read_markets():
    return list_markets_service()


@router.get("/{market_id}")
def read_market(
    market_id: int,
):
    return get_market_service(market_id)