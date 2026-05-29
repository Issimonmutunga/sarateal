from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.data_sources.prices import RawPriceRecord
from app.services import price_ingestion


def test_resolve_product_for_price_record_returns_exact_product_match(monkeypatch):
    matched_product = SimpleNamespace(id=1, name="Maize")

    def fake_find_product_by_name(db, product_name):
        assert product_name == "Maize"
        return matched_product

    def fake_find_product_by_alias(db, source_name, source_product_name):
        raise AssertionError("Alias lookup should not run when exact product exists")

    monkeypatch.setattr(
        price_ingestion,
        "find_product_by_name",
        fake_find_product_by_name,
    )
    monkeypatch.setattr(
        price_ingestion,
        "find_product_by_alias",
        fake_find_product_by_alias,
    )

    record = RawPriceRecord(
        product_name="Maize",
        county="Eastern",
        unit="90 KG",
        price=Decimal("4500"),
        observed_on=date(2026, 4, 15),
        source_name="World Food Programme Kenya Food Prices",
    )

    product = price_ingestion.resolve_product_for_price_record(
        db=SimpleNamespace(),
        record=record,
    )

    assert product == matched_product


def test_resolve_product_for_price_record_falls_back_to_alias(monkeypatch):
    matched_product = SimpleNamespace(id=1, name="Maize")

    def fake_find_product_by_name(db, product_name):
        assert product_name == "Maize (white, dry)"
        return None

    def fake_find_product_by_alias(db, source_name, source_product_name):
        assert source_name == "World Food Programme Kenya Food Prices"
        assert source_product_name == "Maize (white, dry)"
        return matched_product

    monkeypatch.setattr(
        price_ingestion,
        "find_product_by_name",
        fake_find_product_by_name,
    )
    monkeypatch.setattr(
        price_ingestion,
        "find_product_by_alias",
        fake_find_product_by_alias,
    )

    record = RawPriceRecord(
        product_name="Maize (white, dry)",
        county="Eastern",
        unit="90 KG",
        price=Decimal("4500"),
        observed_on=date(2026, 4, 15),
        source_name="World Food Programme Kenya Food Prices",
    )

    product = price_ingestion.resolve_product_for_price_record(
        db=SimpleNamespace(),
        record=record,
    )

    assert product == matched_product


def test_resolve_product_for_price_record_returns_none_when_no_match(monkeypatch):
    def fake_find_product_by_name(db, product_name):
        return None

    def fake_find_product_by_alias(db, source_name, source_product_name):
        return None

    monkeypatch.setattr(
        price_ingestion,
        "find_product_by_name",
        fake_find_product_by_name,
    )
    monkeypatch.setattr(
        price_ingestion,
        "find_product_by_alias",
        fake_find_product_by_alias,
    )

    record = RawPriceRecord(
        product_name="Unknown product variant",
        county="Eastern",
        unit="90 KG",
        price=Decimal("4500"),
        observed_on=date(2026, 4, 15),
        source_name="World Food Programme Kenya Food Prices",
    )

    product = price_ingestion.resolve_product_for_price_record(
        db=SimpleNamespace(),
        record=record,
    )

    assert product is None