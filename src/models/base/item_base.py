from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field

class ItemBase(SQLModel):
    code: int = Field(nullable=False, index=True)
    designation: str = Field(nullable=False, max_length=50, index=True)
    size: Optional[str] = Field(default=None, max_length=50, nullable=True)

    weight: Decimal = Field(default=Decimal("0.0000"), ge=0, nullable=False)

    is_unavailable: bool = Field(default=False, nullable=False)

    points: int = Field(default=0, ge=0, nullable=False)

# A garder pour le moment
    order_by_postal_card: int = Field(default=0, ge=0, nullable=False)
    display_order: int = Field(default=0, ge=0, nullable=False)
    order_by_impression: int = Field(default=0, ge=0, nullable=False)
    order_by_display: int = Field(default=0, ge=0, nullable=False)