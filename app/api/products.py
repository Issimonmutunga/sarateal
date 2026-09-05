from fastapi import APIRouter, Query

from app.services.products import get_product_service, list_products_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def list_products_endpoint(
    active_only: bool = Query(default=True),
):
    return list_products_service(active_only=active_only)


@router.get("/{product_id}")
def get_product_endpoint(
    product_id: int,
):
    return get_product_service(product_id)