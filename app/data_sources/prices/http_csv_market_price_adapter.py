import csv
from collections.abc import Mapping
from datetime import date
from decimal import Decimal
from io import StringIO
from urllib.request import Request, urlopen

from app.data_sources.prices.kenya_market_price_adapter import (
    KenyaMarketPriceRecord,
)


class HttpCsvKenyaMarketPriceAdapter:
    def __init__(
        self,
        source_url: str,
        source_name: str,
        column_map: Mapping[str, str] | None = None,
    ) -> None:
        self.source_url = source_url
        self.source_name = source_name
        self.column_map = column_map or {
            "product_name": "product_name",
            "county": "county",
            "unit": "unit",
            "price": "price",
            "currency": "currency",
            "observed_on": "observed_on",
            "market_name": "market_name",
            "notes": "notes",
        }

    def fetch_prices(self) -> list[KenyaMarketPriceRecord]:
        csv_text = self._fetch_csv_text()
        return self._parse_csv_text(csv_text)

    def _fetch_csv_text(self) -> str:
        request = Request(
            self.source_url,
            headers={"User-Agent": "sarateal-price-adapter/0.1"},
        )

        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")

    def _parse_csv_text(self, csv_text: str) -> list[KenyaMarketPriceRecord]:
        reader = csv.DictReader(StringIO(csv_text))
        records: list[KenyaMarketPriceRecord] = []

        for row in reader:
            records.append(
                KenyaMarketPriceRecord(
                    product_name=self._required(row, "product_name"),
                    county=self._required(row, "county"),
                    unit=self._required(row, "unit"),
                    price=Decimal(self._required(row, "price")),
                    currency=self._required(row, "currency"),
                    observed_on=date.fromisoformat(
                        self._required(row, "observed_on"),
                    ),
                    source_name=self.source_name,
                    source_url=self.source_url,
                    market_name=self._optional(row, "market_name"),
                    notes=self._optional(row, "notes"),
                )
            )

        return records

    def _required(self, row: Mapping[str, str | None], field_name: str) -> str:
        column_name = self.column_map[field_name]
        value = row.get(column_name)

        if value is None or value.strip() == "":
            raise ValueError(f"Missing required price field: {column_name}")

        return value.strip()

    def _optional(self, row: Mapping[str, str | None], field_name: str) -> str | None:
        column_name = self.column_map.get(field_name)

        if column_name is None:
            return None

        value = row.get(column_name)

        if value is None or value.strip() == "":
            return None

        return value.strip()