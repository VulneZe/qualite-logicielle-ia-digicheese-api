from __future__ import annotations

import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class UpdateItemLink(SQLModel, table=True):
    __tablename__ = "update_items"

    # Liaison vers une Update (CASCADE si update supprimée)
    update_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("updates.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )

    # Liaison vers un Item (CASCADE si item supprimé)
    item_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey("items.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )

    # Quantité liée à CET item dans CETTE update
    quantity_update: int = Field(nullable=False)