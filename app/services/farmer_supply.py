from sqlalchemy.orm import Session

from app.core.exceptions import ErrorDetail
from app.core.validators import (
    collect_date_order_error,
    collect_non_negative_number_error,
    collect_positive_number_error,
    raise_if_details,
)
from app.models.farmer_supply import FarmerSupply
from app.schemas.farmer_supply import FarmerSupplyCreate
from app.services.farmers import get_farmer_or_raise
from app.services.products import get_product_or_raise


def validate_farmer_supply(
    db: Session,
    supply_in: FarmerSupplyCreate,
) -> None:
    get_farmer_or_raise(db=db, farmer_id=supply_in.farmer_id)
    get_product_or_raise(db=db, product_id=supply_in.product_id)

    details: list[ErrorDetail] = []

    collect_positive_number_error(
        details=details,
        value=supply_in.quantity,
        field="quantity",
    )
    collect_date_order_error(
        details=details,
        start_date=supply_in.available_from,
        end_date=supply_in.available_until,
        start_field="available_from",
        end_field="available_until",
    )
    collect_non_negative_number_error(
        details=details,
        value=supply_in.expected_price_per_unit,
        field="expected_price_per_unit",
    )

    raise_if_details(
        details=details,
        message="Farmer supply validation failed.",
        entity="FarmerSupply",
        context={
            "farmer_id": supply_in.farmer_id,
            "product_id": supply_in.product_id,
        },
    )


def create_farmer_supply(
    db: Session,
    supply_in: FarmerSupplyCreate,
) -> FarmerSupply:
    validate_farmer_supply(db=db, supply_in=supply_in)

    supply = FarmerSupply(**supply_in.model_dump())

    db.add(supply)
    db.commit()
    db.refresh(supply)

    return supply


def list_farmer_supply(
    db: Session,
    status: str | None = "available",
) -> list[FarmerSupply]:
    query = db.query(FarmerSupply)

    if status:
        query = query.filter(FarmerSupply.status == status)

    return query.order_by(FarmerSupply.available_from).all()


def get_farmer_supply(
    db: Session,
    supply_id: int,
) -> FarmerSupply | None:
    return db.query(FarmerSupply).filter(FarmerSupply.id == supply_id).first()


def list_supply_by_farmer(
    db: Session,
    farmer_id: int,
) -> list[FarmerSupply]:
    get_farmer_or_raise(db=db, farmer_id=farmer_id)

    return (
        db.query(FarmerSupply)
        .filter(FarmerSupply.farmer_id == farmer_id)
        .order_by(FarmerSupply.available_from)
        .all()
    )