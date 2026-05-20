from sqlalchemy.orm import Session

from app.core.exceptions import ErrorDetail
from app.core.validators import (
    collect_date_order_error,
    collect_non_negative_number_error,
    raise_if_details,
    validate_url,
)
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

    collect_non_negative_number_error(
        details=details,
        value=tender_in.quantity,
        field="quantity",
    )
    collect_date_order_error(
        details=details,
        start_date=tender_in.opening_date,
        end_date=tender_in.closing_date,
        start_field="opening_date",
        end_field="closing_date",
    )

    raise_if_details(
        details=details,
        message="Tender validation failed.",
        entity="Tender",
        context={
            "title": tender_in.title,
            "source_name": tender_in.source_name,
        },
    )

    validate_url(
        value=tender_in.source_url,
        field="source_url",
        entity="Tender",
        required=False,
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


def get_tender_or_raise(
    db: Session,
    tender_id: int,
) -> Tender:
    tender = get_tender(db=db, tender_id=tender_id)

    if not tender:
        from app.core.exceptions import record_not_found_error

        raise record_not_found_error(
            entity="Tender",
            identifier=tender_id,
        )

    return tender


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