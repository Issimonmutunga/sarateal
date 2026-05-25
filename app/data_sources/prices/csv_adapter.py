import csv
from datetime import date
from pathlib import Path

from app.data_sources.prices.base import RawPriceRecord, normalize_price_text


REQUIRED_COLUMNS = {
    "product_name",
    "county",
    "unit",
    "price",
    "observed_on",
    "source_name",
}


def parse_price_date(value: str) -> date:
    return date.fromisoformat(value)


def parse_optional_float(value: str | None, default: float) -> float:
    cleaned = normalize_price_text(value)

    if cleaned is None:
        return default

    return float(cleaned)


def validate_csv_columns(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        raise ValueError("CSV file has no header row.")

    missing_columns = REQUIRED_COLUMNS - set(fieldnames)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV file is missing required columns: {missing}")


def read_price_csv(file_path: str | Path) -> list[RawPriceRecord]:
    path = Path(file_path)

    records = []

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        validate_csv_columns(reader.fieldnames)

        for row in reader:
            records.append(
                RawPriceRecord(
                    product_name=normalize_price_text(row.get("product_name")) or "",
                    county=normalize_price_text(row.get("county")) or "",
                    unit=normalize_price_text(row.get("unit")) or "",
                    price=float(normalize_price_text(row.get("price")) or 0),
                    observed_on=parse_price_date(
                        normalize_price_text(row.get("observed_on")) or ""
                    ),
                    source_name=normalize_price_text(row.get("source_name")) or "",
                    market_name=normalize_price_text(row.get("market_name")),
                    source_url=normalize_price_text(row.get("source_url")),
                    confidence_score=parse_optional_float(
                        row.get("confidence_score"),
                        default=1.0,
                    ),
                    notes=normalize_price_text(row.get("notes")),
                )
            )

    return records