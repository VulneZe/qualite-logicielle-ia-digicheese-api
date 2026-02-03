from __future__ import annotations

from typing import Optional

from sqlmodel import Field

from src.models.base.stock_base import StockBase


class Stock(StockBase, table=True):
    __tablename__ = "stocks"

    # PK 
    id: Optional[int] = Field(default=None, primary_key=True)