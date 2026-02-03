from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field

from src.models.base.stock_line_base import StockLineBase


class StockLine(StockLineBase, table=True):
    __tablename__ = "stock_lines"

    # PK technique
    id: Optional[int] = Field(default=None, primary_key=True)

    # Ligne de stock rattachée à un Item (obligatoire)
    # CASCADE : si l'item est supprimé, les lignes associées sont supprimées côté DB
    item_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("items.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    # Stock optionnel (0..1)
    # SET NULL : si le stock est supprimé, la ligne reste mais stock_id devient NULL
    stock_id: Optional[int] = Field(
        default=None,
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("stocks.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        ),
    )