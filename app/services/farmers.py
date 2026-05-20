from sqlalchemy.orm import Session

from app.core.exceptions import duplicate_record_error, record_not_found_error
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate


def create_farmer(db: Session, farmer_in: FarmerCreate) -> Farmer:
    existing_farmer = get_farmer_by_phone(
        db=db,
        phone_number=farmer_in.phone_number,
    )

    if existing_farmer:
        raise duplicate_record_error(
            entity="Farmer",
            field="phone_number",
            value=farmer_in.phone_number,
        )

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


def get_farmer_or_raise(db: Session, farmer_id: int) -> Farmer:
    farmer = get_farmer(db=db, farmer_id=farmer_id)

    if not farmer:
        raise record_not_found_error(
            entity="Farmer",
            identifier=farmer_id,
        )

    return farmer


def get_farmer_by_phone(db: Session, phone_number: str) -> Farmer | None:
    return db.query(Farmer).filter(Farmer.phone_number == phone_number).first()