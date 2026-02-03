from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class StockLineCreate(SQLModel):
    item_id: int = Field(nullable=False)

    # 0..1
    stock_id: Optional[int] = Field(default=None)

    designation: str = Field(max_length=50)

    date_start: Optional[date] = None
    date_end: Optional[date] = None

    quantity_stock: int = Field(default=0, ge=0)