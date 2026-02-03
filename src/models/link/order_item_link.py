from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlmodel import SQLModel, Field

from src.enum.parcel_type_enum import ParcelTypeEnum


class OrderItemLink(SQLModel, table=True):
    __tablename__ = "order_items"

    # PK composite (commande_id, item_id) => 1 ligne par couple
    commande_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("commande.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
            index=True,
        )
    )

    item_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("items.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
            index=True,
        )
    )

    quantity_order: int = Field(nullable=False)

    colis: ParcelTypeEnum = Field(
        sa_column=sa.Column(
            sa.Enum(ParcelTypeEnum, name="parcel_type_enum", native_enum=False),
            nullable=False,
            index=True,
        )
    )

    comment: Optional[str] = Field(default=None, max_length=255, nullable=True)
