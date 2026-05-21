import pytest

from app.core.exceptions import DuplicateRecordError
from app.schemas.buyer import BuyerCreate
from app.schemas.farmer import FarmerCreate
from app.services.buyers import create_buyer
from app.services.farmers import create_farmer


def test_create_farmer_rejects_duplicate_phone_number(db_session):
    create_farmer(
        db=db_session,
        farmer_in=FarmerCreate(
            full_name="Test Farmer One",
            phone_number="0700000001",
            county="Meru",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_farmer(
            db=db_session,
            farmer_in=FarmerCreate(
                full_name="Test Farmer Two",
                phone_number="0700000001",
                county="Nakuru",
            ),
        )


def test_create_buyer_rejects_duplicate_name(db_session):
    create_buyer(
        db=db_session,
        buyer_in=BuyerCreate(
            name="Test Buyer",
            buyer_type="aggregator",
            county="Meru",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_buyer(
            db=db_session,
            buyer_in=BuyerCreate(
                name="Test Buyer",
                buyer_type="retailer",
                county="Nakuru",
            ),
        )


def test_create_buyer_rejects_duplicate_email_when_email_is_provided(db_session):
    create_buyer(
        db=db_session,
        buyer_in=BuyerCreate(
            name="Buyer One",
            buyer_type="aggregator",
            county="Meru",
            email="buyer@example.com",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_buyer(
            db=db_session,
            buyer_in=BuyerCreate(
                name="Buyer Two",
                buyer_type="retailer",
                county="Nakuru",
                email="buyer@example.com",
            ),
        )