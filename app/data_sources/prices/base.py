from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RawPriceRecord:
    product_name: str
    county: str
    unit: str
    price: float
    observed_on: date
    source_name: str
    market_name: str | None = None
    source_url: str | None = None
    confidence_score: float = 1.0
    notes: str | None = None


def normalize_price_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = " ".join(value.strip().split())

    if not cleaned:
        return None

    return cleaned


def normalize_raw_price_record(record: RawPriceRecord) -> RawPriceRecord:
    return RawPriceRecord(
        product_name=normalize_price_text(record.product_name) or record.product_name,
        county=normalize_price_text(record.county) or record.county,
        unit=normalize_price_text(record.unit) or record.unit,
        price=record.price,
        observed_on=record.observed_on,
        source_name=normalize_price_text(record.source_name) or record.source_name,
        market_name=normalize_price_text(record.market_name),
        source_url=normalize_price_text(record.source_url),
        confidence_score=record.confidence_score,
        notes=normalize_price_text(record.notes),
    )