from datetime import date

import pytest

from app.core.exceptions import BusinessRuleViolationError, RecordNotFoundError
from app.schemas.buyer import BuyerCreate
from app.schemas.buyer_demand import BuyerDemandCreate
from app.schemas.farmer import FarmerCreate
from app.schemas.farmer_supply import FarmerSupplyCreate
from app.schemas.product import ProductCreate
from app.services.buyer_demand import create_buyer_demand
from app.services.buyers import create_buyer
from app.services.farmer_supply import create_farmer_supply
from app.services.farmers import create_farmer
from app.services.products import create_product


def create_test_farmer(db_session):
    return create_farmer(
        db=db_session,
        farmer_in=FarmerCreate(
            full_name="Test Farmer",
            phone_number="0700000001",
            county="Meru",
        ),
    )


def create_test_buyer(db_session):
    return create_buyer(
        db=db_session,
        buyer_in=BuyerCreate(
            name="Test Buyer",
            buyer_type="aggregator",
            county="Meru",
        ),
    )


def create_test_product(db_session):
    return create_product(
        db=db_session,
        product_in=ProductCreate(
            name="Test Product",
            category="crop",
            unit="kg",
        ),
    )


def test_create_farmer_supply_rejects_unknown_farmer(db_session):
    with pytest.raises(RecordNotFoundError):
        create_farmer_supply(
            db=db_session,
            supply_in=FarmerSupplyCreate(
                farmer_id=999999,
                product_id=999999,
                quantity=100,
                unit="kg",
                available_from=date(2026, 1, 1),
                available_until=date(2026, 1, 31),
                county="Meru",
            ),
        )


def test_create_farmer_supply_rejects_non_positive_quantity(db_session):
    farmer = create_test_farmer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_farmer_supply(
            db=db_session,
            supply_in=FarmerSupplyCreate(
                farmer_id=farmer.id,
                product_id=product.id,
                quantity=0,
                unit="kg",
                available_from=date(2026, 1, 1),
                available_until=date(2026, 1, 31),
                county="Meru",
            ),
        )


def test_create_farmer_supply_rejects_invalid_date_order(db_session):
    farmer = create_test_farmer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_farmer_supply(
            db=db_session,
            supply_in=FarmerSupplyCreate(
                farmer_id=farmer.id,
                product_id=product.id,
                quantity=100,
                unit="kg",
                available_from=date(2026, 1, 31),
                available_until=date(2026, 1, 1),
                county="Meru",
            ),
        )


def test_create_buyer_demand_rejects_unknown_buyer(db_session):
    with pytest.raises(RecordNotFoundError):
        create_buyer_demand(
            db=db_session,
            demand_in=BuyerDemandCreate(
                buyer_id=999999,
                product_id=999999,
                quantity_needed=100,
                unit="kg",
                needed_from=date(2026, 1, 1),
                needed_until=date(2026, 1, 31),
                county="Meru",
            ),
        )


def test_create_buyer_demand_rejects_non_positive_quantity(db_session):
    buyer = create_test_buyer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_buyer_demand(
            db=db_session,
            demand_in=BuyerDemandCreate(
                buyer_id=buyer.id,
                product_id=product.id,
                quantity_needed=0,
                unit="kg",
                needed_from=date(2026, 1, 1),
                needed_until=date(2026, 1, 31),
                county="Meru",
            ),
        )


def test_create_buyer_demand_rejects_invalid_date_order(db_session):
    buyer = create_test_buyer(db_session)
    product = create_test_product(db_session)

    with pytest.raises(BusinessRuleViolationError):
        create_buyer_demand(
            db=db_session,
            demand_in=BuyerDemandCreate(
                buyer_id=buyer.id,
                product_id=product.id,
                quantity_needed=100,
                unit="kg",
                needed_from=date(2026, 1, 31),
                needed_until=date(2026, 1, 1),
                county="Meru",
            ),
        )