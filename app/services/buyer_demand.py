from sqlalchemy.orm import Session

from app.core.exceptions import ErrorDetail
from app.core.validators import (
    collect_date_order_error,
    collect_non_negative_number_error,
    collect_positive_number_error,
    raise_if_details,
)
from app.models.buyer_demand import BuyerDemand
from app.schemas.buyer_demand import BuyerDemandCreate
from app.services.buyers import get_buyer_or_raise
from app.services.products import get_product_or_raise


def validate_buyer_demand(
    db: Session,
    demand_in: BuyerDemandCreate,
) -> None:
    get_buyer_or_raise(db=db, buyer_id=demand_in.buyer_id)
    get_product_or_raise(db=db, product_id=demand_in.product_id)

    details: list[ErrorDetail] = []

    collect_positive_number_error(
        details=details,
        value=demand_in.quantity_needed,
        field="quantity_needed",
    )
    collect_date_order_error(
        details=details,
        start_date=demand_in.needed_from,
        end_date=demand_in.needed_until,
        start_field="needed_from",
        end_field="needed_until",
    )
    collect_non_negative_number_error(
        details=details,
        value=demand_in.target_price_per_unit,
        field="target_price_per_unit",
    )

    raise_if_details(
        details=details,
        message="Buyer demand validation failed.",
        entity="BuyerDemand",
        context={
            "buyer_id": demand_in.buyer_id,
            "product_id": demand_in.product_id,
        },
    )


def create_buyer_demand(
    db: Session,
    demand_in: BuyerDemandCreate,
) -> BuyerDemand:
    validate_buyer_demand(db=db, demand_in=demand_in)

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
    get_buyer_or_raise(db=db, buyer_id=buyer_id)

    return (
        db.query(BuyerDemand)
        .filter(BuyerDemand.buyer_id == buyer_id)
        .order_by(BuyerDemand.needed_from)
        .all()
    )