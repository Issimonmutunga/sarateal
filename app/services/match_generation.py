from sqlalchemy.orm import Session

from app.models.buyer import Buyer
from app.models.buyer_demand import BuyerDemand
from app.models.farmer import Farmer
from app.models.farmer_supply import FarmerSupply
from app.models.match import Match
from app.services.matching import score_supply_against_demand


def match_exists(
    db: Session,
    farmer_supply_id: int,
    buyer_demand_id: int,
) -> bool:
    return (
        db.query(Match)
        .filter(
            Match.farmer_supply_id == farmer_supply_id,
            Match.buyer_demand_id == buyer_demand_id,
        )
        .first()
        is not None
    )


def generate_supply_demand_matches(db: Session) -> list[Match]:
    supplies = (
        db.query(FarmerSupply)
        .filter(FarmerSupply.status == "available")
        .all()
    )

    demands = (
        db.query(BuyerDemand)
        .filter(BuyerDemand.status == "open")
        .all()
    )

    created_matches: list[Match] = []

    for supply in supplies:
        farmer = db.query(Farmer).filter(Farmer.id == supply.farmer_id).first()

        for demand in demands:
            if supply.product_id != demand.product_id:
                continue

            if match_exists(
                db=db,
                farmer_supply_id=supply.id,
                buyer_demand_id=demand.id,
            ):
                continue

            buyer = db.query(Buyer).filter(Buyer.id == demand.buyer_id).first()

            score, label = score_supply_against_demand(
                supply=supply,
                demand=demand,
                farmer=farmer,
                buyer=buyer,
            )

            match = Match(
                farmer_supply_id=supply.id,
                buyer_demand_id=demand.id,
                opportunity_score=score,
                risk_level="unknown",
                recommendation=(
                    f"{label} opportunity based on product, location, "
                    "volume, and timing fit."
                ),
                status="suggested",
            )

            db.add(match)
            created_matches.append(match)

    db.commit()

    for match in created_matches:
        db.refresh(match)

    return created_matches