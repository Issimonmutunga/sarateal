from app.data_sources.prices.http_csv_market_price_adapter import (
    HttpCsvKenyaMarketPriceAdapter,
)

WFP_KENYA_FOOD_PRICES_CSV_URL = (
    "https://data.humdata.org/dataset/e0d3fba6-f9a2-45d7-b949-140c455197ff/"
    "resource/517ee1bf-2437-4f8c-aa1b-cb9925b9d437/download/"
    "wfp_food_prices_ken.csv"
)


class WfpKenyaPriceAdapter(HttpCsvKenyaMarketPriceAdapter):
    def __init__(self) -> None:
        super().__init__(
            source_url=WFP_KENYA_FOOD_PRICES_CSV_URL,
            source_name="World Food Programme Kenya Food Prices",
            column_map={
                "product_name": "commodity",
                "county": "admin1",
                "unit": "unit",
                "price": "price",
                "currency": "currency",
                "observed_on": "date",
                "market_name": "market",
                "notes": "priceflag",
            },
        )