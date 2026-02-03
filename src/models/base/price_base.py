from __future__ import annotations

from decimal import Decimal
from sqlmodel import SQLModel, Field

class PriceBase(SQLModel):
    unit_price: Decimal = Field(default=Decimal("0.0000"), ge=0, nullable=False)