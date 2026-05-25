import argparse
from pathlib import Path

from app.db.session import SessionLocal
from app.services.price_csv_ingestion import ingest_price_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest Sarateal price records from a CSV file."
    )

    parser.add_argument(
        "file_path",
        type=Path,
        help="Path to the price CSV file.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    db = SessionLocal()

    try:
        prices = ingest_price_csv(
            db=db,
            file_path=args.file_path,
        )

        print(f"Price CSV ingested successfully. Prices created: {len(prices)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()