from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.services.products import create_product, get_product, list_products

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead)
def create_product_endpoint(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
):
    return create_product(db=db, product_in=product_in)


@router.get("/", response_model=list[ProductRead])
def list_products_endpoint(
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    return list_products(db=db, active_only=active_only)


@router.get("/{product_id}", response_model=ProductRead | None)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_product(db=db, product_id=product_id)