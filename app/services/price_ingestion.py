from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_sources.prices import RawPriceRecord, normalize_raw_price_record
from app.models.market import Market
from app.models.product import Product
from app.schemas.price import PriceCreate
from app.services.prices import create_price
from app.services.product_aliases import find_product_by_alias


def find_product_by_name(db: Session, product_name: str) -> Product | None:
    statement = select(Product).where(Product.name == product_name)

    return db.scalar(statement)


def find_market_by_name_and_county(
    db: Session,
    market_name: str,
    county: str,
) -> Market | None:
    statement = select(Market).where(
        Market.name == market_name,
        Market.county == county,
    )

    return db.scalar(statement)


def resolve_product_for_price_record(
    db: Session,
    record: RawPriceRecord,
) -> Product | None:
    product = find_product_by_name(
        db=db,
        product_name=record.product_name,
    )

    if product:
        return product

    return find_product_by_alias(
        db=db,
        source_name=record.source_name,
        source_product_name=record.product_name,
    )


def ingest_raw_price_record(
    db: Session,
    record: RawPriceRecord,
):
    normalized_record = normalize_raw_price_record(record)

    product = resolve_product_for_price_record(
        db=db,
        record=normalized_record,
    )

    if not product:
        return None

    market_id = None

    if normalized_record.market_name:
        market = find_market_by_name_and_county(
            db=db,
            market_name=normalized_record.market_name,
            county=normalized_record.county,
        )

        if market:
            market_id = market.id

    return create_price(
        db=db,
        price_in=PriceCreate(
            product_id=product.id,
            market_id=market_id,
            county=normalized_record.county,
            unit=normalized_record.unit,
            price=normalized_record.price,
            observed_on=normalized_record.observed_on,
            source_name=normalized_record.source_name,
            source_url=normalized_record.source_url,
            confidence_score=normalized_record.confidence_score,
            notes=normalized_record.notes,
        ),
    )


def ingest_raw_price_records(
    db: Session,
    records: list[RawPriceRecord],
):
    created_prices = []

    for record in records:
        price = ingest_raw_price_record(db=db, record=record)

        if price:
            created_prices.append(price)

    return created_prices