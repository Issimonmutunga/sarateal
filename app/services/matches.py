from sqlalchemy.orm import Session

from app.models.match import Match
from app.schemas.match import MatchCreate


def create_match(
    db: Session,
    match_in: MatchCreate,
) -> Match:
    match = Match(**match_in.model_dump())

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def list_matches(
    db: Session,
    status: str | None = "suggested",
) -> list[Match]:
    query = db.query(Match)

    if status:
        query = query.filter(Match.status == status)

    return query.order_by(Match.opportunity_score.desc()).all()


def get_match(
    db: Session,
    match_id: int,
) -> Match | None:
    return db.query(Match).filter(Match.id == match_id).first()


def list_matches_by_supply(
    db: Session,
    farmer_supply_id: int,
) -> list[Match]:
    return (
        db.query(Match)
        .filter(Match.farmer_supply_id == farmer_supply_id)
        .order_by(Match.opportunity_score.desc())
        .all()
    )