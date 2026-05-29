from app.data_sources.prices.wfp_kenya_price_adapter import (
    WFP_KENYA_FOOD_PRICES_CSV_URL,
    WfpKenyaPriceAdapter,
)


def test_wfp_kenya_price_adapter_uses_hdx_csv_url():
    adapter = WfpKenyaPriceAdapter()

    assert adapter.source_url == WFP_KENYA_FOOD_PRICES_CSV_URL
    assert "data.humdata.org" in adapter.source_url
    assert adapter.source_url.endswith("wfp_food_prices_ken.csv")


def test_wfp_kenya_price_adapter_uses_wfp_source_name():
    adapter = WfpKenyaPriceAdapter()

    assert adapter.source_name == "World Food Programme Kenya Food Prices"


def test_wfp_kenya_price_adapter_maps_hdx_columns_to_price_fields():
    adapter = WfpKenyaPriceAdapter()

    assert adapter.column_map == {
        "product_name": "commodity",
        "county": "admin1",
        "unit": "unit",
        "price": "price",
        "currency": "currency",
        "observed_on": "date",
        "market_name": "market",
        "notes": "priceflag",
    }