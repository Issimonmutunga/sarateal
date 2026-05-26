from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.stored_locations import list_stored_locations


router = APIRouter(
    prefix="/stored-locations",
    tags=["Stored Locations"],
)


@router.get("")
def list_cached_locations(
    country: str | None = Query(default=None, min_length=1),
    verified_only: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_stored_locations(
        db=db,
        country=country,
        verified_only=verified_only,
    )