from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleViolationError, ErrorDetail
from app.models.tender import Tender
from app.schemas.tender import TenderCreate
from app.services.buyers import get_buyer_or_raise
from app.services.products import get_product_or_raise


def validate_tender(
    db: Session,
    tender_in: TenderCreate,
) -> None:
    details: list[ErrorDetail] = []

    if tender_in.buyer_id is not None:
        get_buyer_or_raise(db=db, buyer_id=tender_in.buyer_id)

    if tender_in.product_id is not None:
        get_product_or_raise(db=db, product_id=tender_in.product_id)

    if tender_in.quantity is not None and tender_in.quantity < 0:
        details.append(
            ErrorDetail(
                field="quantity",
                message="Tender quantity cannot be negative.",
                value=tender_in.quantity,
            )
        )

    if tender_in.opening_date and tender_in.closing_date:
        if tender_in.closing_date < tender_in.opening_date:
            details.append(
                ErrorDetail(
                    field="closing_date",
                    message="Closing date cannot be earlier than opening date.",
                    value=tender_in.closing_date,
                )
            )

    if tender_in.source_url and not tender_in.source_url.startswith(("http://", "https://")):
        details.append(
            ErrorDetail(
                field="source_url",
                message="Source URL must start with http:// or https://.",
                value=tender_in.source_url,
            )
        )

    if details:
        raise BusinessRuleViolationError(
            message="Tender validation failed.",
            details=details,
            context={
                "entity": "Tender",
                "title": tender_in.title,
                "source_name": tender_in.source_name,
            },
        )


def create_tender(
    db: Session,
    tender_in: TenderCreate,
) -> Tender:
    validate_tender(db=db, tender_in=tender_in)

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