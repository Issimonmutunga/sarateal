from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.buyer import BuyerCreate, BuyerRead
from app.services.buyers import create_buyer, get_buyer, list_buyers

router = APIRouter(prefix="/buyers", tags=["Buyers"])


@router.post("/", response_model=BuyerRead)
def create_buyer_endpoint(
    buyer_in: BuyerCreate,
    db: Session = Depends(get_db),
):
    return create_buyer(db=db, buyer_in=buyer_in)


@router.get("/", response_model=list[BuyerRead])
def list_buyers_endpoint(
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    return list_buyers(db=db, active_only=active_only)


@router.get("/{buyer_id}", response_model=BuyerRead | None)
def get_buyer_endpoint(
    buyer_id: int,
    db: Session = Depends(get_db),
):
    return get_buyer(db=db, buyer_id=buyer_id)