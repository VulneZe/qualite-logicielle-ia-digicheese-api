from datetime import date as dt_date
from typing import Optional

from sqlmodel import SQLModel, Field


class ShopUpdate(SQLModel):
    item_id: Optional[int] = None

    date: Optional[dt_date] = None
    quantity_shop: Optional[int] = Field(default=None, ge=0)