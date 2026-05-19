from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, product_in: ProductCreate) -> Product:
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