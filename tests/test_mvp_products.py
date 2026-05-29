from app.data_sources.mvp_products import MVP_PRODUCTS


def test_mvp_products_include_core_food_products():
    product_names = {product["name"] for product in MVP_PRODUCTS}

    assert "Maize" in product_names
    assert "Beans" in product_names
    assert "Potatoes" in product_names
    assert "Tomatoes" in product_names
    assert "Onions" in product_names
    assert "Cabbage" in product_names
    assert "Kale" in product_names
    assert "Rice" in product_names
    assert "Sorghum" in product_names
    assert "Cowpeas" in product_names


def test_mvp_products_have_required_fields():
    for product in MVP_PRODUCTS:
        assert product["name"]
        assert product["category"]
        assert product["unit"]


def test_mvp_product_names_are_unique():
    product_names = [product["name"] for product in MVP_PRODUCTS]

    assert len(product_names) == len(set(product_names))