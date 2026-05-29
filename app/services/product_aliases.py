from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.product_alias import ProductAlias


def normalize_product_alias_name(product_name: str) -> str:
    return " ".join(
        product_name.strip().lower().replace("(", " ").replace(")", " ").split()
    )


def find_product_by_alias(
    db: Session,
    source_name: str,
    source_product_name: str,
) -> Product | None:
    normalized_name = normalize_product_alias_name(source_product_name)

    statement = (
        select(Product)
        .join(ProductAlias, ProductAlias.product_id == Product.id)
        .where(ProductAlias.source_name == source_name)
        .where(ProductAlias.normalized_name == normalized_name)
    )

    return db.scalar(statement)