from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateRecordError, record_not_found_error
from app.models.market import Market
from app.schemas.market import MarketCreate


def list_markets(db: Session) -> list[Market]:
    statement = select(Market).order_by(Market.county, Market.name)

    return list(db.scalars(statement).all())


def get_market(db: Session, market_id: int) -> Market | None:
    return db.get(Market, market_id)


def get_market_or_raise(db: Session, market_id: int) -> Market:
    market = get_market(db=db, market_id=market_id)

    if not market:
        raise record_not_found_error(
            entity="Market",
            identifier=market_id,
        )

    return market


def create_market(db: Session, market_in: MarketCreate) -> Market:
    existing_market = db.scalar(
        select(Market).where(
            Market.name == market_in.name,
            Market.county == market_in.county,
        )
    )

    if existing_market:
        raise DuplicateRecordError(
            message="Market already exists.",
            details=[],
            context={
                "entity": "Market",
                "name": market_in.name,
                "county": market_in.county,
            },
        )

    market = Market(**market_in.model_dump())

    db.add(market)
    db.commit()
    db.refresh(market)

    return market