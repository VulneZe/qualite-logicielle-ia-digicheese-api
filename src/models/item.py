from __future__ import annotations

from typing import Optional

from sqlmodel import Field
from sqlalchemy import UniqueConstraint

from src.models.base.item_base import ItemBase


class Item(ItemBase, table=True):
    """
    - id = clé technique (PK) : stable, parfaite pour les relations (FK)
    - code = clé métier : unique, utile côté business (référence produit)
    """
    __tablename__ = "items"

    # Garantit en base : 1 seul item par code (sinon doublons possibles)
    __table_args__ = (UniqueConstraint("code", name="uq_items_code"),)

    id: Optional[int] = Field(default=None, primary_key=True)