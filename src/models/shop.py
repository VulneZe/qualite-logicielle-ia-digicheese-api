from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field

from src.models.base.shop_base import ShopBase


class Shop(ShopBase, table=True):
    __tablename__ = "shops"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 1 shop -> 1 item
    item_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("items.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )