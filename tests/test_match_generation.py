from datetime import date, timedelta

from app.models.buyer import Buyer
from app.models.buyer_demand import BuyerDemand
from app.models.farmer import Farmer
from app.models.farmer_supply import FarmerSupply
from app.models.product import Product
from app.services.match_generation import generate_supply_demand_matches


def test_generate_supply_demand_matches_creates_match_for_same_product(db_session):
    product = Product(name="Maize", category="cereal", unit="kg")
    farmer = Farmer(
        full_name="Test Farmer",
        phone_number="0700000001",
        county="Meru",
        is_verified=True,
    )
    buyer = Buyer(
        name="Test Buyer",
        buyer_type="aggregator",
        county="Meru",
        is_verified=True,
    )

    db_session.add_all([product, farmer, buyer])
    db_session.commit()

    db_session.refresh(product)
    db_session.refresh(farmer)
    db_session.refresh(buyer)

    supply = FarmerSupply(
        farmer_id=farmer.id,
        product_id=product.id,
        quantity=1000,
        unit="kg",
        available_from=date.today(),
        available_until=date.today() + timedelta(days=10),
        county="Meru",
        status="available",
    )
    demand = BuyerDemand(
        buyer_id=buyer.id,
        product_id=product.id,
        quantity_needed=800,
        unit="kg",
        needed_from=date.today(),
        needed_until=date.today() + timedelta(days=5),
        county="Meru",
        status="open",
    )

    db_session.add_all([supply, demand])
    db_session.commit()

    matches = generate_supply_demand_matches(db=db_session)

    assert len(matches) == 1
    assert matches[0].farmer_supply_id == supply.id
    assert matches[0].buyer_demand_id == demand.id
    assert matches[0].opportunity_score > 0
    assert matches[0].recommendation is not None


def test_generate_supply_demand_matches_does_not_duplicate_existing_matches(db_session):
    product = Product(name="Potatoes", category="tuber", unit="kg")
    farmer = Farmer(
        full_name="Test Farmer",
        phone_number="0700000002",
        county="Meru",
        is_verified=True,
    )
    buyer = Buyer(
        name="Test Buyer",
        buyer_type="aggregator",
        county="Meru",
        is_verified=True,
    )

    db_session.add_all([product, farmer, buyer])
    db_session.commit()

    db_session.refresh(product)
    db_session.refresh(farmer)
    db_session.refresh(buyer)

    supply = FarmerSupply(
        farmer_id=farmer.id,
        product_id=product.id,
        quantity=1000,
        unit="kg",
        available_from=date.today(),
        available_until=date.today() + timedelta(days=10),
        county="Meru",
        status="available",
    )
    demand = BuyerDemand(
        buyer_id=buyer.id,
        product_id=product.id,
        quantity_needed=800,
        unit="kg",
        needed_from=date.today(),
        needed_until=date.today() + timedelta(days=5),
        county="Meru",
        status="open",
    )

    db_session.add_all([supply, demand])
    db_session.commit()

    first_run = generate_supply_demand_matches(db=db_session)
    second_run = generate_supply_demand_matches(db=db_session)

    assert len(first_run) == 1
    assert len(second_run) == 0


def test_generate_supply_demand_matches_skips_different_products(db_session):
    supply_product = Product(name="Tomatoes", category="vegetable", unit="kg")
    demand_product = Product(name="Onions", category="vegetable", unit="kg")
    farmer = Farmer(
        full_name="Test Farmer",
        phone_number="0700000003",
        county="Meru",
        is_verified=True,
    )
    buyer = Buyer(
        name="Test Buyer",
        buyer_type="aggregator",
        county="Meru",
        is_verified=True,
    )

    db_session.add_all([supply_product, demand_product, farmer, buyer])
    db_session.commit()

    db_session.refresh(supply_product)
    db_session.refresh(demand_product)
    db_session.refresh(farmer)
    db_session.refresh(buyer)

    supply = FarmerSupply(
        farmer_id=farmer.id,
        product_id=supply_product.id,
        quantity=1000,
        unit="kg",
        available_from=date.today(),
        available_until=date.today() + timedelta(days=10),
        county="Meru",
        status="available",
    )
    demand = BuyerDemand(
        buyer_id=buyer.id,
        product_id=demand_product.id,
        quantity_needed=800,
        unit="kg",
        needed_from=date.today(),
        needed_until=date.today() + timedelta(days=5),
        county="Meru",
        status="open",
    )

    db_session.add_all([supply, demand])
    db_session.commit()

    matches = generate_supply_demand_matches(db=db_session)

    assert matches == []