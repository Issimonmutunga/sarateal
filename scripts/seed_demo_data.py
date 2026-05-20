from datetime import date, timedelta

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.buyer import Buyer
from app.models.buyer_demand import BuyerDemand
from app.models.farmer import Farmer
from app.models.farmer_supply import FarmerSupply
from app.models.product import Product
from app.services.match_generation import generate_supply_demand_matches


def get_product_id(db, name: str) -> int:
    product = db.query(Product).filter(Product.name == name).first()

    if not product:
        raise ValueError(f"Product not found: {name}. Run scripts\\seed_base_data.py first.")

    return product.id


def seed_demo_data() -> None:
    init_db()
    db = SessionLocal()

    try:
        maize_id = get_product_id(db, "Maize")
        beans_id = get_product_id(db, "Beans")
        potatoes_id = get_product_id(db, "Potatoes")

        farmer_1 = Farmer(
            full_name="Demo Farmer Eldoret",
            phone_number="0700000001",
            county="Uasin Gishu",
            sub_county="Ainabkoi",
            ward="Kapsoya",
            farmer_group="Demo Maize Group",
            is_verified=True,
        )
        farmer_2 = Farmer(
            full_name="Demo Farmer Meru",
            phone_number="0700000002",
            county="Meru",
            sub_county="Imenti North",
            ward="Municipality",
            farmer_group="Demo Potato Group",
            is_verified=False,
        )

        buyer_1 = Buyer(
            name="Demo Nairobi School Feeding Buyer",
            buyer_type="institution",
            contact_person="Procurement Officer",
            phone_number="0710000001",
            email="buyer1@example.com",
            county="Nairobi",
            is_verified=True,
        )
        buyer_2 = Buyer(
            name="Demo Meru Aggregator",
            buyer_type="aggregator",
            contact_person="Supply Manager",
            phone_number="0710000002",
            email="buyer2@example.com",
            county="Meru",
            is_verified=True,
        )

        db.add_all([farmer_1, farmer_2, buyer_1, buyer_2])
        db.commit()

        db.refresh(farmer_1)
        db.refresh(farmer_2)
        db.refresh(buyer_1)
        db.refresh(buyer_2)

        today = date.today()

        supplies = [
            FarmerSupply(
                farmer_id=farmer_1.id,
                product_id=maize_id,
                quantity=3000,
                unit="kg",
                available_from=today,
                available_until=today + timedelta(days=21),
                county="Uasin Gishu",
                sub_county="Ainabkoi",
                ward="Kapsoya",
                expected_price_per_unit=55,
            ),
            FarmerSupply(
                farmer_id=farmer_2.id,
                product_id=potatoes_id,
                quantity=1500,
                unit="kg",
                available_from=today + timedelta(days=7),
                available_until=today + timedelta(days=30),
                county="Meru",
                sub_county="Imenti North",
                ward="Municipality",
                expected_price_per_unit=45,
            ),
        ]

        demands = [
            BuyerDemand(
                buyer_id=buyer_1.id,
                product_id=maize_id,
                quantity_needed=2500,
                unit="kg",
                needed_from=today + timedelta(days=3),
                needed_until=today + timedelta(days=25),
                county="Nairobi",
                target_price_per_unit=60,
                requirements="Clean dry maize suitable for institutional supply.",
            ),
            BuyerDemand(
                buyer_id=buyer_2.id,
                product_id=potatoes_id,
                quantity_needed=1200,
                unit="kg",
                needed_from=today + timedelta(days=5),
                needed_until=today + timedelta(days=20),
                county="Meru",
                target_price_per_unit=50,
                requirements="Sorted potatoes for aggregation.",
            ),
            BuyerDemand(
                buyer_id=buyer_2.id,
                product_id=beans_id,
                quantity_needed=800,
                unit="kg",
                needed_from=today,
                needed_until=today + timedelta(days=14),
                county="Meru",
                target_price_per_unit=130,
                requirements="Dry beans.",
            ),
        ]

        db.add_all(supplies + demands)
        db.commit()

        matches = generate_supply_demand_matches(db=db)

        print(f"Sarateal demo data seeded successfully. Matches created: {len(matches)}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()