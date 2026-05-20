from sqlalchemy.orm import Session

from app.core.exceptions import duplicate_record_error, record_not_found_error
from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, product_in: ProductCreate) -> Product:
    existing_product = get_product_by_name(
        db=db,
        name=product_in.name,
    )

    if existing_product:
        raise duplicate_record_error(
            entity="Product",
            field="name",
            value=product_in.name,
        )

    product = Product(**product_in.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def list_products(db: Session, active_only: bool = True) -> list[Product]:
    query = db.query(Product)

    if active_only:
        query = query.filter(Product.is_active.is_(True))

    return query.order_by(Product.name).all()


def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_or_raise(db: Session, product_id: int) -> Product:
    product = get_product(db=db, product_id=product_id)

    if not product:
        raise record_not_found_error(
            entity="Product",
            identifier=product_id,
        )

    return product


def get_product_by_name(db: Session, name: str) -> Product | None:
    return db.query(Product).filter(Product.name == name).first()