from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProductAlias(Base):
    __tablename__ = "product_aliases"

    __table_args__ = (
        UniqueConstraint(
            "source_name",
            "source_product_name",
            name="uq_product_alias_source_product",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    source_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    source_product_name: Mapped[str] = mapped_column(String, nullable=False)
    normalized_name: Mapped[str] = mapped_column(String, nullable=False, index=True)