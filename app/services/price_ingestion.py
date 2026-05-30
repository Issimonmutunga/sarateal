from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_sources.prices import RawPriceRecord, normalize_raw_price_record
from app.models.market import Market
from app.models.price import Price
from app.models.product import Product
from app.schemas.price import PriceCreate
from app.services.prices import create_price, find_existing_price
from app.services.product_aliases import find_product_by_alias


@dataclass(frozen=True)
class PriceIngestionSummary:
    total_records: int
    created_count: int
    existing_count: int
    unmatched_count: int
    prices: list[Price]


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


def build_price_create_from_raw_record(
    db: Session,
    record: RawPriceRecord,
) -> PriceCreate | None:
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

    return PriceCreate(
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
    )


def ingest_raw_price_record(
    db: Session,
    record: RawPriceRecord,
):
    price_in = build_price_create_from_raw_record(
        db=db,
        record=record,
    )

    if not price_in:
        return None

    return create_price(
        db=db,
        price_in=price_in,
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


def ingest_raw_price_records_with_summary(
    db: Session,
    records: list[RawPriceRecord],
) -> PriceIngestionSummary:
    prices: list[Price] = []
    created_count = 0
    existing_count = 0
    unmatched_count = 0

    for record in records:
        price_in = build_price_create_from_raw_record(
            db=db,
            record=record,
        )

        if not price_in:
            unmatched_count += 1
            continue

        existing_price = find_existing_price(
            db=db,
            price_in=price_in,
        )

        if existing_price:
            existing_count += 1
            prices.append(existing_price)
            continue

        price = create_price(
            db=db,
            price_in=price_in,
        )
        created_count += 1
        prices.append(price)

    return PriceIngestionSummary(
        total_records=len(records),
        created_count=created_count,
        existing_count=existing_count,
        unmatched_count=unmatched_count,
        prices=prices,
    )