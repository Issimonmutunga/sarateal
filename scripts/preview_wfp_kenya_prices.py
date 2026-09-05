from app.data_sources.prices.wfp_kenya_price_adapter import WfpKenyaPriceAdapter


def main() -> None:
    adapter = WfpKenyaPriceAdapter()
    records = adapter.fetch_prices()

    print(f"Fetched {len(records)} WFP Kenya price records")

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


if __name__ == "__main__":
    main()