from app.data_sources.kenya_counties import KENYA_COUNTIES
from app.data_sources.mvp_products import MVP_PRODUCTS
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.county import County
from app.models.product import Product


def seed_counties(db) -> None:
    for county_data in KENYA_COUNTIES:
        existing = db.query(County).filter(County.code == county_data["code"]).first()

        if existing:
            continue

        db.add(County(**county_data))


def seed_products(db) -> None:
    for product_data in MVP_PRODUCTS:
        existing = db.query(Product).filter(Product.name == product_data["name"]).first()

        if existing:
            continue

        db.add(Product(**product_data))


def seed_base_data() -> None:
    init_db()

    db = SessionLocal()

    try:
        seed_counties(db)
        seed_products(db)
        db.commit()
        print("Sarateal base data seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_base_data()