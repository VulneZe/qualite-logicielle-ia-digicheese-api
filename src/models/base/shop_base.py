from __future__ import annotations

from datetime import date as dt_date

from sqlmodel import SQLModel, Field


class ShopBase(SQLModel):
    # Date associée à l’entrée boutique
    date: dt_date = Field(default_factory=dt_date.today, nullable=False)

    # Quantité associée à l’entrée boutique
    quantity_shop: int = Field(default=0, ge=0, nullable=False)