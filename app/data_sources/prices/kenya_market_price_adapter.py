from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class KenyaMarketPriceRecord:
    product_name: str
    county: str
    unit: str
    price: Decimal
    currency: str
    observed_on: date
    source_name: str
    source_url: str | None = None
    market_name: str | None = None
    notes: str | None = None


class KenyaMarketPriceAdapter(Protocol):
    def fetch_prices(self) -> list[KenyaMarketPriceRecord]:
        """Fetch Kenya market price records from an external or structured source."""