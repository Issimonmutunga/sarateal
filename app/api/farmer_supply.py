from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.farmer_supply import FarmerSupplyCreate, FarmerSupplyRead
from app.services.farmer_supply import (
    create_farmer_supply,
    get_farmer_supply,
    list_farmer_supply,
    list_supply_by_farmer,
)

router = APIRouter(prefix="/farmer-supply", tags=["Farmer Supply"])


@router.post("/", response_model=FarmerSupplyRead)
def create_farmer_supply_endpoint(
    supply_in: FarmerSupplyCreate,
    db: Session = Depends(get_db),
):
    return create_farmer_supply(db=db, supply_in=supply_in)


@router.get("/", response_model=list[FarmerSupplyRead])
def list_farmer_supply_endpoint(
    status: str | None = "available",
    db: Session = Depends(get_db),
):
    return list_farmer_supply(db=db, status=status)


@router.get("/{supply_id}", response_model=FarmerSupplyRead | None)
def get_farmer_supply_endpoint(
    supply_id: int,
    db: Session = Depends(get_db),
):
    return get_farmer_supply(db=db, supply_id=supply_id)


@router.get("/farmer/{farmer_id}", response_model=list[FarmerSupplyRead])
def list_supply_by_farmer_endpoint(
    farmer_id: int,
    db: Session = Depends(get_db),
):
    return list_supply_by_farmer(db=db, farmer_id=farmer_id)