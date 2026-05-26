from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.geocoding import geocode_location_name_with_cache


router = APIRouter(
    prefix="/geocoding",
    tags=["Geocoding"],
)


@router.get("/search")
def search_geocoded_locations(
    location_name: str = Query(..., min_length=1),
    country: str = Query(default="Kenya", min_length=1),
    limit: int = Query(default=1, ge=1, le=5),
    db: Session = Depends(get_db),
):
    return geocode_location_name_with_cache(
        db=db,
        location_name=location_name,
        country=country,
        limit=limit,
    )