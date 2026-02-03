from __future__ import annotations

from decimal import Decimal
from sqlmodel import SQLModel


class PriceRead(SQLModel):
    id: int
    item_id: int
    unit_price: Decimal