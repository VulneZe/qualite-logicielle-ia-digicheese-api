from __future__ import annotations

from datetime import datetime
from sqlmodel import SQLModel, Field


class UpdateBase(SQLModel):
    # Type de mise à jour (ex: STOCK, CORRECTION, INVENTORY)
    update_type: str = Field(nullable=False, max_length=30, index=True)

    # Date de la mise à jour
    update_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)