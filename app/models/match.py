from datetime import datetime

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    farmer_supply_id: Mapped[int] = mapped_column(
        ForeignKey("farmer_supply.id"),
        nullable=False,
        index=True,
    )
    buyer_demand_id: Mapped[int | None] = mapped_column(
        ForeignKey("buyer_demand.id"),
        nullable=True,
        index=True,
    )
    tender_id: Mapped[int | None] = mapped_column(
        ForeignKey("tenders.id"),
        nullable=True,
        index=True,
    )

    opportunity_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_transport_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_margin: Mapped[float | None] = mapped_column(Float, nullable=True)

    risk_level: Mapped[str] = mapped_column(String(50), default="unknown", nullable=False)
    recommendation: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="suggested", nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)