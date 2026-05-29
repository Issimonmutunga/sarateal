from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import record_not_found_error
from app.core.validators import (
    validate_non_negative_number,
    validate_score_range,
    validate_url,
)
from app.models.market import Market
from app.models.price import Price
from app.models.product import Product
from app.schemas.price import PriceCreate


def list_prices(db: Session) -> list[Price]:
    statement = select(Price).order_by(
        Price.observed_on.desc(),
        Price.county,
        Price.product_id,
    )

    return list(db.scalars(statement).all())


def get_price(db: Session, price_id: int) -> Price | None:
    return db.get(Price, price_id)


def get_price_or_raise(db: Session, price_id: int) -> Price:
    price = get_price(db=db, price_id=price_id)

    if not price:
        raise record_not_found_error(
            entity="Price",
            identifier=price_id,
        )

    return price


def find_existing_price(db: Session, price_in: PriceCreate) -> Price | None:
    statement = select(Price).where(
        Price.product_id == price_in.product_id,
        Price.market_id == price_in.market_id,
        Price.county == price_in.county,
        Price.unit == price_in.unit,
        Price.price == price_in.price,
        Price.observed_on == price_in.observed_on,
        Price.source_name == price_in.source_name,
    )

    return db.scalar(statement)


def validate_price(db: Session, price_in: PriceCreate) -> None:
    product = db.get(Product, price_in.product_id)

    if not product:
        raise record_not_found_error(
            entity="Product",
            identifier=price_in.product_id,
        )

    if price_in.market_id is not None:
        market = db.get(Market, price_in.market_id)

        if not market:
            raise record_not_found_error(
                entity="Market",
                identifier=price_in.market_id,
            )

    validate_non_negative_number(
        price_in.price,
        field="price",
        entity="Price",
    )
    validate_score_range(
        price_in.confidence_score,
        field="confidence_score",
        entity="Price",
        minimum=0.0,
        maximum=1.0,
    )
    validate_url(
        price_in.source_url,
        field="source_url",
        entity="Price",
    )


def create_price(db: Session, price_in: PriceCreate) -> Price:
    validate_price(db=db, price_in=price_in)

    existing_price = find_existing_price(
        db=db,
        price_in=price_in,
    )

    if existing_price:
        return existing_price

    price = Price(**price_in.model_dump())

    db.add(price)
    db.commit()
    db.refresh(price)

    return price