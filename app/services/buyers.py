from sqlalchemy.orm import Session

from app.models.buyer import Buyer
from app.schemas.buyer import BuyerCreate


def create_buyer(db: Session, buyer_in: BuyerCreate) -> Buyer:
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