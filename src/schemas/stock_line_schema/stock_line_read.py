from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel


class StockLineRead(SQLModel):
    id: int
    item_id: int
    stock_id: Optional[int] = None

    designation: str

    date_start: Optional[date] = None
    date_end: Optional[date] = None

    quantity_stock: int