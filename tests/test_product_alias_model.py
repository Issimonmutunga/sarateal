from app.models.product_alias import ProductAlias


def test_product_alias_model_stores_external_product_mapping():
    alias = ProductAlias(
        product_id=1,
        source_name="World Food Programme Kenya Food Prices",
        source_product_name="Maize (white, dry)",
        normalized_name="maize white dry",
    )

    assert alias.product_id == 1
    assert alias.source_name == "World Food Programme Kenya Food Prices"
    assert alias.source_product_name == "Maize (white, dry)"
    assert alias.normalized_name == "maize white dry"


def test_product_alias_table_name_is_product_aliases():
    assert ProductAlias.__tablename__ == "product_aliases"