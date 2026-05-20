from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tender import TenderCreate, TenderRead
from app.services.tenders import (
    create_tender,
    get_tender,
    list_tenders,
    list_tenders_by_county,
)

router = APIRouter(prefix="/tenders", tags=["Tenders"])


@router.post("/", response_model=TenderRead)
def create_tender_endpoint(
    tender_in: TenderCreate,
    db: Session = Depends(get_db),
):
    return create_tender(db=db, tender_in=tender_in)


@router.get("/", response_model=list[TenderRead])
def list_tenders_endpoint(
    status: str | None = "open",
    db: Session = Depends(get_db),
):
    return list_tenders(db=db, status=status)


@router.get("/county/{county}", response_model=list[TenderRead])
def list_tenders_by_county_endpoint(
    county: str,
    db: Session = Depends(get_db),
):
    return list_tenders_by_county(db=db, county=county)


@router.get("/{tender_id}", response_model=TenderRead | None)
def get_tender_endpoint(
    tender_id: int,
    db: Session = Depends(get_db),
):
    return get_tender(db=db, tender_id=tender_id)