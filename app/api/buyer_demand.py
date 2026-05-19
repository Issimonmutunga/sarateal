from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.buyer_demand import BuyerDemandCreate, BuyerDemandRead
from app.services.buyer_demand import (
    create_buyer_demand,
    get_buyer_demand,
    list_buyer_demand,
    list_demand_by_buyer,
)

router = APIRouter(prefix="/buyer-demand", tags=["Buyer Demand"])


@router.post("/", response_model=BuyerDemandRead)
def create_buyer_demand_endpoint(
    demand_in: BuyerDemandCreate,
    db: Session = Depends(get_db),
):
    return create_buyer_demand(db=db, demand_in=demand_in)


@router.get("/", response_model=list[BuyerDemandRead])
def list_buyer_demand_endpoint(
    status: str | None = "open",
    db: Session = Depends(get_db),
):
    return list_buyer_demand(db=db, status=status)


@router.get("/{demand_id}", response_model=BuyerDemandRead | None)
def get_buyer_demand_endpoint(
    demand_id: int,
    db: Session = Depends(get_db),
):
    return get_buyer_demand(db=db, demand_id=demand_id)


@router.get("/buyer/{buyer_id}", response_model=list[BuyerDemandRead])
def list_demand_by_buyer_endpoint(
    buyer_id: int,
    db: Session = Depends(get_db),
):
    return list_demand_by_buyer(db=db, buyer_id=buyer_id)