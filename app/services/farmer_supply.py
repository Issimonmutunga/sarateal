from sqlalchemy.orm import Session

from app.models.farmer_supply import FarmerSupply
from app.schemas.farmer_supply import FarmerSupplyCreate


def create_farmer_supply(
    db: Session,
    supply_in: FarmerSupplyCreate,
) -> FarmerSupply:
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
    return (
        db.query(FarmerSupply)
        .filter(FarmerSupply.farmer_id == farmer_id)
        .order_by(FarmerSupply.available_from)
        .all()
    )