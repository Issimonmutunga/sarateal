from sqlalchemy.orm import Session

from app.models.buyer_demand import BuyerDemand
from app.schemas.buyer_demand import BuyerDemandCreate


def create_buyer_demand(
    db: Session,
    demand_in: BuyerDemandCreate,
) -> BuyerDemand:
    demand = BuyerDemand(**demand_in.model_dump())

    db.add(demand)
    db.commit()
    db.refresh(demand)

    return demand


def list_buyer_demand(
    db: Session,
    status: str | None = "open",
) -> list[BuyerDemand]:
    query = db.query(BuyerDemand)

    if status:
        query = query.filter(BuyerDemand.status == status)

    return query.order_by(BuyerDemand.needed_from).all()


def get_buyer_demand(
    db: Session,
    demand_id: int,
) -> BuyerDemand | None:
    return db.query(BuyerDemand).filter(BuyerDemand.id == demand_id).first()


def list_demand_by_buyer(
    db: Session,
    buyer_id: int,
) -> list[BuyerDemand]:
    return (
        db.query(BuyerDemand)
        .filter(BuyerDemand.buyer_id == buyer_id)
        .order_by(BuyerDemand.needed_from)
        .all()
    )