from app.data_sources.prices.base import RawPriceRecord
from app.data_sources.prices.kenya_market_price_adapter import (
    KenyaMarketPriceAdapter,
)


def fetch_raw_price_records_from_adapter(
    adapter: KenyaMarketPriceAdapter,
) -> list[RawPriceRecord]:
    records = adapter.fetch_prices()

    return [
        RawPriceRecord(
            product_name=record.product_name,
            county=record.county,
            unit=record.unit,
            price=record.price,
            observed_on=record.observed_on,
            source_name=record.source_name,
            source_url=record.source_url,
            notes=_build_notes(record.market_name, record.notes),
        )
        for record in records
    ]


def _build_notes(market_name: str | None, notes: str | None) -> str | None:
    note_parts: list[str] = []

    if market_name:
        note_parts.append(f"Market: {market_name}")

    if notes:
        note_parts.append(notes)

    if not note_parts:
        return None

    return " | ".join(note_parts)