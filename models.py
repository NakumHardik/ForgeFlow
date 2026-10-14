from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price_per_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    stock_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )