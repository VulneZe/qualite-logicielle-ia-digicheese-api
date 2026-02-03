from __future__ import annotations

import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class ConditionnementItemLink(SQLModel, table=True):
    __tablename__ = "conditionnement_items"

    __table_args__ = (
        sa.CheckConstraint(
            "quantity_min <= quantity_max",
            name="ck_conditionnement_items_qty_min_le_max",
        ),
    )

    # PK composite : 1 ligne par couple (conditionnement, item)
    conditionnement_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("conditionnement.id", ondelete="CASCADE"),
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

    quantity_min: int = Field(nullable=False)
    quantity_max: int = Field(nullable=False)