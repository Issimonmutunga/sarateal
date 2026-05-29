from sqlalchemy import select

from app.data_sources.prices.wfp_kenya_price_adapter import WfpKenyaPriceAdapter
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.product import Product
from app.models.product_alias import ProductAlias
from app.services.product_aliases import normalize_product_alias_name


WFP_SOURCE_NAME = "World Food Programme Kenya Food Prices"

WFP_PRODUCT_ALIAS_MAP = {
    "Maize": [
        "Maize",
        "Maize (white)",
        "Maize (white, dry)",
    ],
    "Beans": [
        "Beans",
        "Beans (dry)",
        "Beans (rosecoco)",
    ],
    "Potatoes": [
        "Potatoes (Irish)",
        "Potatoes (Irish, red)",
        "Potatoes (Irish, white)",
    ],
    "Tomatoes": [
        "Tomatoes",
    ],
    "Onions": [
        "Onions",
        "Onions (dry)",
    ],
    "Cabbage": [
        "Cabbage",
    ],
    "Kale": [
        "Kale",
    ],
    "Rice": [
        "Rice",
        "Rice (imported)",
        "Rice (local)",
    ],
    "Sorghum": [
        "Sorghum",
    ],
    "Cowpeas": [
        "Cowpeas",
    ],
}


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
    init_db()

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


def main() -> None:
    created_count = seed_wfp_product_aliases()

    print(f"Created {created_count} WFP product aliases")
    print(f"Source adapter: {WfpKenyaPriceAdapter.__name__}")


if __name__ == "__main__":
    main()