import argparse

from app.data_sources.prices.wfp_kenya_price_adapter import WfpKenyaPriceAdapter
from app.db.session import SessionLocal
from app.services.kenya_market_price_ingestion import (
    fetch_raw_price_records_from_adapter,
)
from app.services.price_ingestion import ingest_raw_price_records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and optionally ingest WFP Kenya food price records.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write matching records to the database. Defaults to dry-run.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum records to process. Use 0 for all records.",
    )

    args = parser.parse_args()

    adapter = WfpKenyaPriceAdapter()
    records = fetch_raw_price_records_from_adapter(adapter)

    if args.limit > 0:
        records = records[: args.limit]

    print(f"Fetched {len(records)} WFP Kenya raw price records")

    if not args.write:
        print("Dry-run only. No records were written to the database.")
        print("Use --write to ingest records.")

        for record in records[:10]:
            print(
                {
                    "product_name": record.product_name,
                    "county": record.county,
                    "unit": record.unit,
                    "price": str(record.price),
                    "observed_on": str(record.observed_on),
                    "source_name": record.source_name,
                    "source_url": record.source_url,
                    "notes": record.notes,
                }
            )

        return

    with SessionLocal() as db:
        created_prices = ingest_raw_price_records(
            db=db,
            records=records,
        )
        db.commit()

    print(f"Created {len(created_prices)} price records")


if __name__ == "__main__":
    main()