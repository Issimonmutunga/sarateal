import pytest

from app.core.exceptions import RecordNotFoundError
from app.services.buyers import get_buyer_or_raise
from app.services.counties import get_county_or_raise
from app.services.farmers import get_farmer_or_raise
from app.services.products import get_product_or_raise
from app.services.tenders import get_tender_or_raise


def test_get_county_or_raise_rejects_unknown_county(db_session):
    with pytest.raises(RecordNotFoundError):
        get_county_or_raise(db=db_session, county_id=999999)


def test_get_product_or_raise_rejects_unknown_product(db_session):
    with pytest.raises(RecordNotFoundError):
        get_product_or_raise(db=db_session, product_id=999999)


def test_get_farmer_or_raise_rejects_unknown_farmer(db_session):
    with pytest.raises(RecordNotFoundError):
        get_farmer_or_raise(db=db_session, farmer_id=999999)


def test_get_buyer_or_raise_rejects_unknown_buyer(db_session):
    with pytest.raises(RecordNotFoundError):
        get_buyer_or_raise(db=db_session, buyer_id=999999)


def test_get_tender_or_raise_rejects_unknown_tender(db_session):
    with pytest.raises(RecordNotFoundError):
        get_tender_or_raise(db=db_session, tender_id=999999)