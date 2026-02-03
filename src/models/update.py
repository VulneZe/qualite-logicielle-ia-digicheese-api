from __future__ import annotations

from typing import Optional
from sqlmodel import Field

from src.models.base.update_base import UpdateBase


class Update(UpdateBase, table=True):
    __tablename__ = "updates"

    # PK technique
    id: Optional[int] = Field(default=None, primary_key=True)