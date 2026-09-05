from app.dataset import get_product, list_products


def list_products_service(active_only: bool = True) -> list:
    return list_products(active_only=active_only)


def get_product_service(product_id: int):
    return get_product(product_id)