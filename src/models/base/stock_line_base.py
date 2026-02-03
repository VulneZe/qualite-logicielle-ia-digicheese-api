from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class StockLineBase(SQLModel):
    # Libellé
    designation: str = Field(nullable=False, max_length=50, index=True)

    # Période optionnelle (NULL si non renseignée)
    date_start: Optional[date] = Field(default=None, nullable=True)
    date_end: Optional[date] = Field(default=None, nullable=True)

    # Quantité en stock (validation >= 0 côté modèle)
    quantity_stock: int = Field(default=0, ge=0, nullable=False)