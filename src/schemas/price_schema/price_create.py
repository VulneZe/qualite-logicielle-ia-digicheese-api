from __future__ import annotations

from decimal import Decimal
from sqlmodel import SQLModel, Field


class PriceCreate(SQLModel):
    item_id: int = Field(nullable=False)
    unit_price: Decimal = Field(ge=0, nullable=False)