from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.farmer import FarmerCreate, FarmerRead
from app.services.farmers import create_farmer, get_farmer, list_farmers

router = APIRouter(prefix="/farmers", tags=["Farmers"])


@router.post("/", response_model=FarmerRead)
def create_farmer_endpoint(
    farmer_in: FarmerCreate,
    db: Session = Depends(get_db),
):
    return create_farmer(db=db, farmer_in=farmer_in)


@router.get("/", response_model=list[FarmerRead])
def list_farmers_endpoint(
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    return list_farmers(db=db, active_only=active_only)


@router.get("/{farmer_id}", response_model=FarmerRead | None)
def get_farmer_endpoint(
    farmer_id: int,
    db: Session = Depends(get_db),
):
    return get_farmer(db=db, farmer_id=farmer_id)