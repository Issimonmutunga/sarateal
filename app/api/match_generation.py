from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.match import MatchRead
from app.services.match_generation import generate_supply_demand_matches

router = APIRouter(prefix="/match-generation", tags=["Match Generation"])


@router.post("/supply-demand", response_model=list[MatchRead])
def generate_supply_demand_matches_endpoint(
    db: Session = Depends(get_db),
):
    return generate_supply_demand_matches(db=db)