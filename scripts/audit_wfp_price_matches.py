from collections import Counter

from app.data_sources.prices.wfp_kenya_price_adapter import WfpKenyaPriceAdapter
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.services.kenya_market_price_ingestion import (
    fetch_raw_price_records_from_adapter,
)
from app.services.price_ingestion import resolve_product_for_price_record


def main() -> None:
    init_db()

    adapter = WfpKenyaPriceAdapter()
    records = fetch_raw_price_records_from_adapter(adapter)
    records = sorted(
        records,
        key=lambda record: record.observed_on,
        reverse=True,
    )

    matched_product_names: Counter[str] = Counter()
    unmatched_product_names: Counter[str] = Counter()

    with SessionLocal() as db:
        for record in records:
            product = resolve_product_for_price_record(
                db=db,
                record=record,
            )

            if product:
                matched_product_names[record.product_name] += 1
            else:
                unmatched_product_names[record.product_name] += 1

    print(f"Audited {len(records)} WFP Kenya price records")
    print(f"Matched source product names: {len(matched_product_names)}")
    print(f"Unmatched source product names: {len(unmatched_product_names)}")

    print("\nTop matched product names:")
    for product_name, count in matched_product_names.most_common(20):
        print(f"- {product_name}: {count}")

    print("\nTop unmatched product names:")
    for product_name, count in unmatched_product_names.most_common(50):
        print(f"- {product_name}: {count}")


if __name__ == "__main__":
    main()