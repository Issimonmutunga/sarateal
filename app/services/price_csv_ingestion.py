from pathlib import Path

from sqlalchemy.orm import Session

from app.data_sources.prices import read_price_csv
from app.services.price_ingestion import ingest_raw_price_records


def ingest_price_csv(
    db: Session,
    file_path: str | Path,
):
    records = read_price_csv(file_path)

    return ingest_raw_price_records(
        db=db,
        records=records,
    )