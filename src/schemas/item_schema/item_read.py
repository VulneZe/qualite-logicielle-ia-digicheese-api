from __future__ import annotations

from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel


class ItemRead(SQLModel):
    id: int

    code: int
    designation: str
    size: Optional[str] = None

    weight: Decimal

    is_unavailable: bool
    points: int

    order_by_postal_card: int
    display_order: int
    order_by_impression: int
    order_by_display: int