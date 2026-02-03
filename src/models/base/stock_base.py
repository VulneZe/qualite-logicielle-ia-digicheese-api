from __future__ import annotations

from sqlmodel import SQLModel, Field


class StockBase(SQLModel):
    # Libellé du stock
    designation: str = Field(nullable=False, max_length=50, index=True)