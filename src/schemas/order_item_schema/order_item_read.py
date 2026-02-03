from __future__ import annotations

from typing import Optional

from sqlmodel import SQLModel

from src.enum.parcel_type_enum import ParcelTypeEnum


class OrderItemRead(SQLModel):
    commande_id: int
    item_id: int
    quantity_order: int
    colis: ParcelTypeEnum
    comment: Optional[str] = None