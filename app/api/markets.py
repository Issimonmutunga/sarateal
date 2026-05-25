from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.market import MarketCreate, MarketRead
from app.services.markets import create_market, get_market_or_raise, list_markets


router = APIRouter(prefix="/markets", tags=["markets"])


@router.get("", response_model=list[MarketRead])
def read_markets(db: Session = Depends(get_db)):
    return list_markets(db=db)


@router.post("", response_model=MarketRead)
def create_market_endpoint(
    market_in: MarketCreate,
    db: Session = Depends(get_db),
):
    return create_market(db=db, market_in=market_in)


@router.get("/{market_id}", response_model=MarketRead)
def read_market(
    market_id: int,
    db: Session = Depends(get_db),
):
    return get_market_or_raise(db=db, market_id=market_id)