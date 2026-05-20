from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleViolationError, ErrorDetail, record_not_found_error
from app.models.match import Match
from app.schemas.match import MatchCreate


def validate_match(match_in: MatchCreate) -> None:
    details: list[ErrorDetail] = []

    if match_in.buyer_demand_id is None and match_in.tender_id is None:
        details.append(
            ErrorDetail(
                field="buyer_demand_id",
                message="A match must reference either buyer_demand_id or tender_id.",
                value=None,
            )
        )

    if match_in.buyer_demand_id is not None and match_in.tender_id is not None:
        details.append(
            ErrorDetail(
                field="tender_id",
                message="A match should reference buyer_demand_id or tender_id, not both.",
                value=match_in.tender_id,
            )
        )

    if match_in.opportunity_score < 0 or match_in.opportunity_score > 100:
        details.append(
            ErrorDetail(
                field="opportunity_score",
                message="Opportunity score must be between 0 and 100.",
                value=match_in.opportunity_score,
            )
        )

    if match_in.estimated_transport_cost is not None and match_in.estimated_transport_cost < 0:
        details.append(
            ErrorDetail(
                field="estimated_transport_cost",
                message="Estimated transport cost cannot be negative.",
                value=match_in.estimated_transport_cost,
            )
        )

    if details:
        raise BusinessRuleViolationError(
            message="Match validation failed.",
            details=details,
            context={
                "entity": "Match",
                "farmer_supply_id": match_in.farmer_supply_id,
                "buyer_demand_id": match_in.buyer_demand_id,
                "tender_id": match_in.tender_id,
            },
        )


def create_match(
    db: Session,
    match_in: MatchCreate,
) -> Match:
    validate_match(match_in=match_in)

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


def get_match_or_raise(
    db: Session,
    match_id: int,
) -> Match:
    match = get_match(db=db, match_id=match_id)

    if not match:
        raise record_not_found_error(
            entity="Match",
            identifier=match_id,
        )

    return match


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