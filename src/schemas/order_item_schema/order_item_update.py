from __future__ import annotations

from typing import Optional

from sqlmodel import SQLModel, Field

from src.enum.parcel_type_enum import ParcelTypeEnum


class OrderItemUpdate(SQLModel):
    quantity_order: Optional[int] = Field(default=None, ge=1)
    colis: Optional[ParcelTypeEnum] = None
    comment: Optional[str] = Field(default=None, max_length=255)