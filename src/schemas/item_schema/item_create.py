from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


class ItemCreate(SQLModel):
    # Obligatoires
    code: int
    designation: str = Field(max_length=50)

    # Optionnel
    size: Optional[str] = Field(default=None, max_length=50)

    # Numériques (défauts si non fournis)
    weight: Decimal = Field(default=Decimal("0.0000"), ge=0)

    # Flags
    is_unavailable: bool = False

    # Divers
    points: int = Field(default=0, ge=0)

    order_by_postal_card: int = Field(default=0, ge=0)
    display_order: int = Field(default=0, ge=0)
    order_by_impression: int = Field(default=0, ge=0)
    order_by_display: int = Field(default=0, ge=0)