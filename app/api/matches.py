from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.match import MatchCreate, MatchRead
from app.services.matches import (
    create_match,
    get_match,
    list_matches,
    list_matches_by_supply,
)

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/", response_model=MatchRead)
def create_match_endpoint(
    match_in: MatchCreate,
    db: Session = Depends(get_db),
):
    return create_match(db=db, match_in=match_in)


@router.get("/", response_model=list[MatchRead])
def list_matches_endpoint(
    status: str | None = "suggested",
    db: Session = Depends(get_db),
):
    return list_matches(db=db, status=status)


@router.get("/{match_id}", response_model=MatchRead | None)
def get_match_endpoint(
    match_id: int,
    db: Session = Depends(get_db),
):
    return get_match(db=db, match_id=match_id)


@router.get("/supply/{farmer_supply_id}", response_model=list[MatchRead])
def list_matches_by_supply_endpoint(
    farmer_supply_id: int,
    db: Session = Depends(get_db),
):
    return list_matches_by_supply(db=db, farmer_supply_id=farmer_supply_id)