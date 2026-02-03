from __future__ import annotations

from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


class PriceUpdate(SQLModel):
    unit_price: Optional[Decimal] = Field(default=None, ge=0)