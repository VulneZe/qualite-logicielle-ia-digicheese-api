from datetime import date as dt_date
from typing import Optional

from sqlmodel import SQLModel, Field


class ShopCreate(SQLModel):
    item_id: int = Field(nullable=False)

    date: dt_date = Field(default_factory=dt_date.today)
    quantity_shop: int = Field(default=0, ge=0)