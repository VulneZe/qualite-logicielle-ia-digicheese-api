from __future__ import annotations

from typing import Optional

from sqlmodel import SQLModel, Field

from src.enum.parcel_type_enum import ParcelTypeEnum


class OrderItemCreate(SQLModel):
    commande_id: int
    item_id: int
    quantity_order: int = Field(ge=1)
    colis: ParcelTypeEnum
    comment: Optional[str] = Field(default=None, max_length=255)