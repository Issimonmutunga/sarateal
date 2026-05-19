from app.db.base import Base
from app.db.session import engine

# Import all models so SQLAlchemy registers them before creating tables.
from app.models import (  # noqa: F401
    Buyer,
    BuyerDemand,
    County,
    Farmer,
    FarmerSupply,
    Match,
    Product,
    Tender,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)