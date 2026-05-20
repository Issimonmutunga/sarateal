from sqlalchemy.orm import Session

from app.core.exceptions import duplicate_record_error, record_not_found_error
from app.models.buyer import Buyer
from app.schemas.buyer import BuyerCreate


def create_buyer(db: Session, buyer_in: BuyerCreate) -> Buyer:
    existing_buyer = get_buyer_by_name(
        db=db,
        name=buyer_in.name,
    )

    if existing_buyer:
        raise duplicate_record_error(
            entity="Buyer",
            field="name",
            value=buyer_in.name,
        )

    if buyer_in.email:
        existing_email = get_buyer_by_email(
            db=db,
            email=buyer_in.email,
        )

        if existing_email:
            raise duplicate_record_error(
                entity="Buyer",
                field="email",
                value=buyer_in.email,
            )

    buyer = Buyer(**buyer_in.model_dump())

    db.add(buyer)
    db.commit()
    db.refresh(buyer)

    return buyer


def list_buyers(db: Session, active_only: bool = True) -> list[Buyer]:
    query = db.query(Buyer)

    if active_only:
        query = query.filter(Buyer.is_active.is_(True))

    return query.order_by(Buyer.name).all()


def get_buyer(db: Session, buyer_id: int) -> Buyer | None:
    return db.query(Buyer).filter(Buyer.id == buyer_id).first()


def get_buyer_or_raise(db: Session, buyer_id: int) -> Buyer:
    buyer = get_buyer(db=db, buyer_id=buyer_id)

    if not buyer:
        raise record_not_found_error(
            entity="Buyer",
            identifier=buyer_id,
        )

    return buyer


def get_buyer_by_name(db: Session, name: str) -> Buyer | None:
    return db.query(Buyer).filter(Buyer.name == name).first()


def get_buyer_by_email(db: Session, email: str) -> Buyer | None:
    return db.query(Buyer).filter(Buyer.email == email).first()