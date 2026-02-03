from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field


class ItemUpdate(SQLModel):
    # Tout optionnel (PATCH)
    code: Optional[int] = None
    designation: Optional[str] = Field(default=None, max_length=50)
    size: Optional[str] = Field(default=None, max_length=50)

    weight: Optional[Decimal] = Field(default=None, ge=0)

    is_unavailable: Optional[bool] = None

    points: Optional[int] = Field(default=None, ge=0)

    order_by_postal_card: Optional[int] = Field(default=None, ge=0)
    display_order: Optional[int] = Field(default=None, ge=0)
    order_by_impression: Optional[int] = Field(default=None, ge=0)
    order_by_display: Optional[int] = Field(default=None, ge=0)