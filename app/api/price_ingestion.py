from pathlib import Path

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.price_csv_ingestion import ingest_price_csv


router = APIRouter(prefix="/price-ingestion", tags=["price-ingestion"])


class PriceCsvIngestionRequest(BaseModel):
    file_path: str


class PriceCsvIngestionResponse(BaseModel):
    prices_created: int


@router.post("/csv", response_model=PriceCsvIngestionResponse)
def ingest_price_csv_endpoint(
    request: PriceCsvIngestionRequest,
    db: Session = Depends(get_db),
):
    prices = ingest_price_csv(
        db=db,
        file_path=Path(request.file_path),
    )

    return PriceCsvIngestionResponse(
        prices_created=len(prices),
    )