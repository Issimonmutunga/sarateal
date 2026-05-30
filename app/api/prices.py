from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.price import PriceCreate, PriceRead
from app.services.prices import create_price, get_price_or_raise, list_prices


router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=list[PriceRead])
def read_prices(
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of latest price records to return.",
    ),
    db: Session = Depends(get_db),
):
    prices = list_prices(db=db)

    return prices[:limit]


@router.post("", response_model=PriceRead)
def create_price_endpoint(
    price_in: PriceCreate,
    db: Session = Depends(get_db),
):
    return create_price(db=db, price_in=price_in)


@router.get("/{price_id}", response_model=PriceRead)
def read_price(
    price_id: int,
    db: Session = Depends(get_db),
):
    return get_price_or_raise(db=db, price_id=price_id)