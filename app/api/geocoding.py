from fastapi import APIRouter, Query

from app.services.geocoding import geocode_location_name


router = APIRouter(
    prefix="/geocoding",
    tags=["Geocoding"],
)


@router.get("/search")
def search_geocoded_locations(
    location_name: str = Query(..., min_length=1),
    country: str = Query(default="Kenya", min_length=1),
    limit: int = Query(default=1, ge=1, le=5),
):
    return geocode_location_name(
        location_name=location_name,
        country=country,
        limit=limit,
    )