from datetime import date

import pytest

from app.core.exceptions import BusinessRuleViolationError, RecordNotFoundError
from app.schemas.buyer import BuyerCreate
from app.schemas.product import ProductCreate
from app.schemas.tender import TenderCreate
from app.services.buyers import create_buyer
from app.services.products import create_product
from app.services.tenders import create_tender


def create_test_buyer(db_session):
    return create_buyer(
        db=db_session,
        buyer_in=BuyerCreate(
            name="Tender Buyer",
            buyer_type="institution",
            county="Meru",
        ),
    )


def create_test_product(db_session):
    return create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Tender Product",
            category="crop",
            unit="kg",
        ),
    )


def create_test_tender_payload(**overrides):
    payload = {
        "title": "Maize Supply Tender",
        "source_name": "Test Source",
        "county": "Meru",
        "quantity": 1000,
        "unit": "kg",
        "opening_date": date(2026, 1, 1),
        "closing_date": date(2026, 1, 31),
    }

    payload.update(overrides)

    return TenderCreate(**payload)


def test_create_tender_rejects_unknown_buyer(db_session):
    product = create_test_product(db_session)

    with pytest.raises(RecordNotFoundError):
        create_tender(
            db=db_session,
            tender_in=create_test_tender_payload(
                buyer_id=999999,
                product_id=product.id,
            ),
        )


def test_create_tender_rejects_unknown_product(db_session):
    buyer = create_test_buyer(db_session)

    with pytest.raises(RecordNotFoundError):
        create_tender(
            db=db_session,
            tender_in=create_test_tender_payload(
                buyer_id=buyer.id,
                product_id=999999,
            ),
        )


def test_create_tender_rejects_negative_quantity(db_session):
    buyer = create_test_buyer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_tender(
            db=db_session,
            tender_in=create_test_tender_payload(
                buyer_id=buyer.id,
                product_id=product.id,
                quantity=-1,
            ),
        )


def test_create_tender_rejects_invalid_date_order(db_session):
    buyer = create_test_buyer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_tender(
            db=db_session,
            tender_in=create_test_tender_payload(
                buyer_id=buyer.id,
                product_id=product.id,
                opening_date=date(2026, 1, 31),
                closing_date=date(2026, 1, 1),
            ),
        )


def test_create_tender_rejects_invalid_source_url(db_session):
    buyer = create_test_buyer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_tender(
            db=db_session,
            tender_in=create_test_tender_payload(
                buyer_id=buyer.id,
                product_id=product.id,
                source_url="ftp://example.com/tender",
            ),
        )