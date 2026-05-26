from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.stored_locations import (
    list_stored_locations,
    set_stored_location_verification,
)


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


@router.patch("/{stored_location_id}/verification")
def update_cached_location_verification(
    stored_location_id: int,
    is_verified: bool,
    db: Session = Depends(get_db),
):
    stored_location = set_stored_location_verification(
        db=db,
        stored_location_id=stored_location_id,
        is_verified=is_verified,
    )

    if stored_location is None:
        raise HTTPException(
            status_code=404,
            detail="Stored location not found.",
        )

    return stored_location