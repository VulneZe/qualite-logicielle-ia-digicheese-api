from __future__ import annotations

from sqlmodel import SQLModel


class ItemDelete(SQLModel):
    id: int
    deleted: bool = True