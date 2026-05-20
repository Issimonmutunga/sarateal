from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleViolationError, ErrorDetail
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

    if supply_in.quantity <= 0:
        details.append(
            ErrorDetail(
                field="quantity",
                message="Supply quantity must be greater than zero.",
                value=supply_in.quantity,
            )
        )

    if supply_in.available_until and supply_in.available_until < supply_in.available_from:
        details.append(
            ErrorDetail(
                field="available_until",
                message="Available until date cannot be earlier than available from date.",
                value=supply_in.available_until,
            )
        )

    if supply_in.expected_price_per_unit is not None and supply_in.expected_price_per_unit < 0:
        details.append(
            ErrorDetail(
                field="expected_price_per_unit",
                message="Expected price per unit cannot be negative.",
                value=supply_in.expected_price_per_unit,
            )
        )

    if details:
        raise BusinessRuleViolationError(
            message="Farmer supply validation failed.",
            details=details,
            context={
                "entity": "FarmerSupply",
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