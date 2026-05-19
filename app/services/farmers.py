from sqlalchemy.orm import Session

from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate


def create_farmer(db: Session, farmer_in: FarmerCreate) -> Farmer:
    farmer = Farmer(**farmer_in.model_dump())

    db.add(farmer)
    db.commit()
    db.refresh(farmer)

    return farmer


def list_farmers(db: Session, active_only: bool = True) -> list[Farmer]:
    query = db.query(Farmer)

    if active_only:
        query = query.filter(Farmer.is_active.is_(True))

    return query.order_by(Farmer.full_name).all()


def get_farmer(db: Session, farmer_id: int) -> Farmer | None:
    return db.query(Farmer).filter(Farmer.id == farmer_id).first()


def get_farmer_by_phone(db: Session, phone_number: str) -> Farmer | None:
    return db.query(Farmer).filter(Farmer.phone_number == phone_number).first()