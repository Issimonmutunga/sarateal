import argparse

from sqlalchemy import select

from app.data_sources.kenya_counties import KENYA_COUNTIES
from app.data_sources.mvp_products import MVP_PRODUCTS
from app.data_sources.prices.wfp_kenya_price_adapter import WfpKenyaPriceAdapter
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.county import County
from app.models.product import Product
from app.models.product_alias import ProductAlias
from app.services.kenya_market_price_ingestion import (
    fetch_raw_price_records_from_adapter,
)
from app.services.price_ingestion import ingest_raw_price_records_with_summary
from app.services.product_aliases import normalize_product_alias_name


WFP_SOURCE_NAME = "World Food Programme Kenya Food Prices"

WFP_PRODUCT_ALIAS_MAP = {
    "Maize": ["Maize", "Maize (white)", "Maize (white, dry)"],
    "Maize Flour": ["Maize flour", "Maize flour (white)"],
    "Wheat Flour": ["Wheat flour"],
    "Rice": ["Rice", "Rice (aromatic)", "Rice (imported)", "Rice (imported, Pakistan)", "Rice (local)"],
    "Sorghum": ["Sorghum", "Sorghum (red)", "Sorghum (white)"],
    "Millet": ["Millet (finger)"],
    "Beans": [
        "Beans",
        "Beans (dry)",
        "Beans (dolichos)",
        "Beans (kidney)",
        "Beans (mung)",
        "Beans (rosecoco)",
        "Beans (yellow)",
    ],
    "Cowpeas": ["Cowpeas", "Cowpeas (dry)"],
    "Pigeon Peas": ["Pigeon peas (dry)"],
    "Potatoes": ["Potatoes (Irish)", "Potatoes (Irish, red)", "Potatoes (Irish, white)"],
    "Tomatoes": ["Tomatoes"],
    "Onions": ["Onions", "Onions (dry)", "Onions (red)"],
    "Cabbage": ["Cabbage"],
    "Kale": ["Kale"],
    "Spinach": ["Spinach"],
    "Bananas": ["Bananas"],
    "Milk": ["Milk (camel, fresh)", "Milk (cow, fresh)", "Milk (cow, pasteurized)", "Milk (UHT)"],
    "Meat": ["Meat (beef)", "Meat (camel)", "Meat (goat)"],
    "Fish": ["Fish (omena, dry)"],
    "Bread": ["Bread"],
    "Sugar": ["Sugar"],
    "Salt": ["Salt"],
    "Cooking Oil": ["Oil (vegetable)", "Oil (vegetable, fortified)"],
    "Cooking Fat": ["Cooking fat"],
}


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


def find_product_by_name(db, product_name: str) -> Product | None:
    statement = select(Product).where(Product.name == product_name)

    return db.scalar(statement)


def product_alias_exists(
    db,
    source_name: str,
    source_product_name: str,
) -> bool:
    normalized_name = normalize_product_alias_name(source_product_name)

    statement = (
        select(ProductAlias)
        .where(ProductAlias.source_name == source_name)
        .where(ProductAlias.normalized_name == normalized_name)
    )

    return db.scalar(statement) is not None


def seed_wfp_product_aliases() -> int:
    created_count = 0

    with SessionLocal() as db:
        for product_name, source_product_names in WFP_PRODUCT_ALIAS_MAP.items():
            product = find_product_by_name(db=db, product_name=product_name)

            if not product:
                print(f"Skipping missing base product: {product_name}")
                continue

            for source_product_name in source_product_names:
                if product_alias_exists(
                    db=db,
                    source_name=WFP_SOURCE_NAME,
                    source_product_name=source_product_name,
                ):
                    continue

                db.add(
                    ProductAlias(
                        product_id=product.id,
                        source_name=WFP_SOURCE_NAME,
                        source_product_name=source_product_name,
                        normalized_name=normalize_product_alias_name(
                            source_product_name,
                        ),
                    )
                )
                created_count += 1

        db.commit()

    return created_count


def sync_wfp_prices(limit: int) -> None:
    init_db()

    with SessionLocal() as db:
        seed_counties(db)
        seed_products(db)
        db.commit()

    alias_count = seed_wfp_product_aliases()

    adapter = WfpKenyaPriceAdapter()
    records = fetch_raw_price_records_from_adapter(adapter)
    records = sorted(
        records,
        key=lambda record: record.observed_on,
        reverse=True,
    )

    if limit > 0:
        records = records[:limit]

    with SessionLocal() as db:
        summary = ingest_raw_price_records_with_summary(
            db=db,
            records=records,
        )
        db.commit()

    print("WFP Kenya price sync complete")
    print(f"Aliases created: {alias_count}")
    print(f"Total records: {summary.total_records}")
    print(f"Inserted records: {summary.created_count}")
    print(f"Existing records: {summary.existing_count}")
    print(f"Unmatched records: {summary.unmatched_count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed lookup data and sync latest WFP Kenya price records.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Maximum newest WFP records to process. Use 0 for all records.",
    )

    args = parser.parse_args()

    sync_wfp_prices(limit=args.limit)


if __name__ == "__main__":
    main()