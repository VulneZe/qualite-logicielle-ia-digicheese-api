from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.item import Item

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship

from src.models.base.price_base import PriceBase


class Price(PriceBase, table=True):
    __tablename__ = "prices"
    __table_args__ = (UniqueConstraint("item_id", name="uq_prices_item_id"),)

    id: int | None = Field(default=None, primary_key=True)

    # FK côté Price + ON DELETE CASCADE côté DB
    item_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("items.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )