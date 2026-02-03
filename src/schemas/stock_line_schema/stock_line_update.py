from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class StockLineUpdate(SQLModel):
    # Tout optionnel (PATCH)
    item_id: Optional[int] = None
    stock_id: Optional[int] = None

    designation: Optional[str] = Field(default=None, max_length=50)

    date_start: Optional[date] = None
    date_end: Optional[date] = None

    quantity_stock: Optional[int] = Field(default=None, ge=0)