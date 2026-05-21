import pytest

from app.core.exceptions import DuplicateRecordError
from app.schemas.county import CountyCreate
from app.schemas.product import ProductCreate
from app.services.counties import create_county
from app.services.products import create_product


def test_create_county_rejects_duplicate_county_code(db_session):
    create_county(
        db=db_session,
        county_in=CountyCreate(
            name="Meru",
            code="MER",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_county(
            db=db_session,
            county_in=CountyCreate(
                name="Meru Different",
                code="MER",
            ),
        )


def test_create_county_rejects_duplicate_county_name(db_session):
    create_county(
        db=db_session,
        county_in=CountyCreate(
            name="Nakuru",
            code="NAK",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_county(
            db=db_session,
            county_in=CountyCreate(
                name="Nakuru",
                code="NAK2",
            ),
        )


def test_create_product_rejects_duplicate_product_name(db_session):
    create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Maize",
            category="cereal",
            unit="kg",
        ),
    )

    with pytest.raises(DuplicateRecordError):
        create_product(
            db=db_session,
            product_in=ProductCreate(
                name="Maize",
                category="grain",
                unit="bag",
            ),
        )