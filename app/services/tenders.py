from sqlalchemy.orm import Session

from app.models.tender import Tender
from app.schemas.tender import TenderCreate


def create_tender(
    db: Session,
    tender_in: TenderCreate,
) -> Tender:
    tender = Tender(**tender_in.model_dump())

    db.add(tender)
    db.commit()
    db.refresh(tender)

    return tender


def list_tenders(
    db: Session,
    status: str | None = "open",
) -> list[Tender]:
    query = db.query(Tender)

    if status:
        query = query.filter(Tender.status == status)

    return query.order_by(Tender.closing_date).all()


def get_tender(
    db: Session,
    tender_id: int,
) -> Tender | None:
    return db.query(Tender).filter(Tender.id == tender_id).first()


def list_tenders_by_county(
    db: Session,
    county: str,
) -> list[Tender]:
    return (
        db.query(Tender)
        .filter(Tender.county == county)
        .order_by(Tender.closing_date)
        .all()
    )