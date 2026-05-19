from datetime import date

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BuyerDemand(Base):
    __tablename__ = "buyer_demand"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    buyer_id: Mapped[int] = mapped_column(
        ForeignKey("buyers.id"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity_needed: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    needed_from: Mapped[date] = mapped_column(nullable=False)
    needed_until: Mapped[date | None] = mapped_column(nullable=True)

    county: Mapped[str] = mapped_column(String(100), nullable=False)
    sub_county: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ward: Mapped[str | None] = mapped_column(String(100), nullable=True)

    target_price_per_unit: Mapped[float | None] = mapped_column(Float, nullable=True)
    requirements: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)