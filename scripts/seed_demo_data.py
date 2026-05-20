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
        raise ValueError(f"Product not found: {name}. Run python -m scripts.seed_base_data first.")

    return product.id


def get_or_create_farmer(db, phone_number: str, **data) -> Farmer:
    farmer = db.query(Farmer).filter(Farmer.phone_number == phone_number).first()

    if farmer:
        return farmer

    farmer = Farmer(phone_number=phone_number, **data)
    db.add(farmer)
    db.commit()
    db.refresh(farmer)

    return farmer


def get_or_create_buyer(db, name: str, **data) -> Buyer:
    buyer = db.query(Buyer).filter(Buyer.name == name).first()

    if buyer:
        return buyer

    buyer = Buyer(name=name, **data)
    db.add(buyer)
    db.commit()
    db.refresh(buyer)

    return buyer


def supply_exists(db, farmer_id: int, product_id: int) -> bool:
    return (
        db.query(FarmerSupply)
        .filter(
            FarmerSupply.farmer_id == farmer_id,
            FarmerSupply.product_id == product_id,
            FarmerSupply.status == "available",
        )
        .first()
        is not None
    )


def demand_exists(db, buyer_id: int, product_id: int) -> bool:
    return (
        db.query(BuyerDemand)
        .filter(
            BuyerDemand.buyer_id == buyer_id,
            BuyerDemand.product_id == product_id,
            BuyerDemand.status == "open",
        )
        .first()
        is not None
    )


def seed_demo_data() -> None:
    init_db()
    db = SessionLocal()

    try:
        maize_id = get_product_id(db, "Maize")
        beans_id = get_product_id(db, "Beans")
        potatoes_id = get_product_id(db, "Potatoes")

        farmer_1 = get_or_create_farmer(
            db,
            phone_number="0700000001",
            full_name="Demo Farmer Eldoret",
            county="Uasin Gishu",
            sub_county="Ainabkoi",
            ward="Kapsoya",
            farmer_group="Demo Maize Group",
            is_verified=True,
        )
        farmer_2 = get_or_create_farmer(
            db,
            phone_number="0700000002",
            full_name="Demo Farmer Meru",
            county="Meru",
            sub_county="Imenti North",
            ward="Municipality",
            farmer_group="Demo Potato Group",
            is_verified=False,
        )

        buyer_1 = get_or_create_buyer(
            db,
            name="Demo Nairobi School Feeding Buyer",
            buyer_type="institution",
            contact_person="Procurement Officer",
            phone_number="0710000001",
            email="buyer1@example.com",
            county="Nairobi",
            is_verified=True,
        )
        buyer_2 = get_or_create_buyer(
            db,
            name="Demo Meru Aggregator",
            buyer_type="aggregator",
            contact_person="Supply Manager",
            phone_number="0710000002",
            email="buyer2@example.com",
            county="Meru",
            is_verified=True,
        )

        today = date.today()

        new_records = []

        if not supply_exists(db, farmer_1.id, maize_id):
            new_records.append(
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
                )
            )

        if not supply_exists(db, farmer_2.id, potatoes_id):
            new_records.append(
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
                )
            )

        if not demand_exists(db, buyer_1.id, maize_id):
            new_records.append(
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
                )
            )

        if not demand_exists(db, buyer_2.id, potatoes_id):
            new_records.append(
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
                )
            )

        if not demand_exists(db, buyer_2.id, beans_id):
            new_records.append(
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
                )
            )

        db.add_all(new_records)
        db.commit()

        matches = generate_supply_demand_matches(db=db)

        print(
            "Sarateal demo data seeded successfully. "
            f"New records: {len(new_records)}. Matches created: {len(matches)}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()