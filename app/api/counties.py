from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.county import CountyCreate, CountyRead
from app.services.counties import create_county, get_county, list_counties

router = APIRouter(prefix="/counties", tags=["Counties"])


@router.post("/", response_model=CountyRead)
def create_county_endpoint(
    county_in: CountyCreate,
    db: Session = Depends(get_db),
):
    return create_county(db=db, county_in=county_in)


@router.get("/", response_model=list[CountyRead])
def list_counties_endpoint(
    db: Session = Depends(get_db),
):
    return list_counties(db=db)


@router.get("/{county_id}", response_model=CountyRead | None)
def get_county_endpoint(
    county_id: int,
    db: Session = Depends(get_db),
):
    return get_county(db=db, county_id=county_id)