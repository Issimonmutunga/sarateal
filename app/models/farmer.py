from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    county: Mapped[str] = mapped_column(String(100), nullable=False)
    sub_county: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ward: Mapped[str | None] = mapped_column(String(100), nullable=True)

    farmer_group: Mapped[str | None] = mapped_column(String(150), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)